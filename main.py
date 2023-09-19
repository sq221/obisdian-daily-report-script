import json
import os
import re
import datetime
import random
import yaml

class Data:
    def __init__(self, metadata) -> None:
        self.date = metadata["Date"]
        self.vault_path = metadata["vaultPath"]
        self.tdpath = os.path.join(metadata["vaultPath"],metadata["TaskDir"])
        self.taskfiles = [os.path.join(self.tdpath,file)  for file in os.listdir(self.tdpath) if file not in metadata["fileToExclude"]]
        self.tasks = {}
        for file in self.taskfiles:
            filename = os.path.splitext(os.path.basename(file))[0]
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
            remain, finish = self.get_task(text)
            self.tasks[filename] = {
                "finish": finish,
                "remain": remain
            }
        self.changes = self.get_change(metadata)
        
    def get_task(self,text):
        # 使用正则表达式查找以 "- [ ]" 开头的行并分类为 "remain"
        remain_tasks = re.findall(r'^- \[ \] (.+)', text, re.MULTILINE)
        # 使用正则表达式查找以 "- [x]" 开头的行并分类为 "finish"
        finish_tasks = re.findall(r'^- \[x\] (.+)', text, re.MULTILINE)
        return remain_tasks, finish_tasks
    
    def get_change(self,metadata):
        new_finish = set([val for file in self.tasks.keys() for val in self.tasks[file]["finish"]])
        new_remain = set([val for file in self.tasks.keys() for val in self.tasks[file]["remain"]])
        old_finish = set(metadata["finished"])
        old_remain = set(metadata["remained"])
        change_finish = list(new_finish-old_finish)
        change_remain = list(new_remain-old_remain)
        sample_size = min(len(new_remain),5)
        display_remain = random.sample(list(new_remain),sample_size)
        return change_finish, change_remain, display_remain, list(new_finish), list(new_remain)
    
class Writer:
    def __init__(self, metadata) -> None:
        self.metadata = metadata
        self.data = Data(metadata)
        self.report_path = os.path.join(metadata["vaultPath"],metadata["reportPath"])
        
    def write(self, dirpath):
        with open(os.path.join(dirpath,"template.md"),"r",encoding="utf-8") as f:
            self.template = f.read()
        content = {
            "date" : str(self.data.date),
            "finish" : "\n- ".join(self.data.changes[0]),
            "newtask" : "\n- ".join(self.data.changes[1]),
            "remain" : "\n- ".join(self.data.changes[2]),
            "num_finish" : len(self.data.changes[0]),
            "num_remain" : len(self.data.changes[4]),
            "remark": ""
        }
        if content["finish"] == "":
            content["finish"] = "什么也没有完成"
        if content["newtask"] == "":
            content["newtask"] = "没有新的任务"
            
        if os.path.exists(os.path.join(self.data.vault_path,f"{self.data.date}.md")):
            with open(os.path.join(self.data.vault_path,f"{self.data.date}.md"), "r", encoding="utf-8") as f:
                content["remark"] = f.read()
            os.remove(os.path.join(self.data.vault_path,f"{self.data.date}.md"))
        self.template = self.template.format(**content)

        with open(self.report_path,"a", encoding="utf-8") as f:
            f.write(self.template)
            
        with open(os.path.join(dirpath,"data.json"),'w',encoding="utf-8") as f:
            data = {
                    "Date": str(datetime.date.today()),
                    "vaultPath": self.metadata["vaultPath"],
                    "TaskDir": self.metadata["TaskDir"],
                    "fileToExclude": self.metadata["fileToExclude"],
                    "reportPath": self.metadata["reportPath"],
                    "finished": self.data.changes[3],
                    "remained": self.data.changes[4]
                    }
            json.dump(data,f)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(script_dir,"data.json")
    if not os.path.exists(datapath):
        configpath=os.path.join(script_dir,"config.yml")
        with open(configpath,"r",encoding="utf-8") as f:
            opt = yaml.load(f,yaml.FullLoader)["Config"]
            assert opt["VaultPath"] != "", "Please fill in the config.yml first!"
            assert opt["TaskDir"] != "", "Please fill in the config.yml first!"
            assert opt["ReportPath"] != "", "Please fill in the config.yml first!"
        print("Initialize data.json")
        with open(datapath,"w",encoding="utf-8") as f:
            data = {
                "Date": str(datetime.date.today()),
                "vaultPath": opt["VaultPath"],
                "TaskDir": opt["TaskDir"],
                "fileToExclude": opt["FileToExclude"],
                "reportPath": opt["ReportPath"],
                "finished": [],
                "remained": []
            }
            init_meta = Data(data)
            data["finished"] = init_meta.changes[3]
            data["remained"] = init_meta.changes[4]
            json.dump(data,f)
            print("Finished!")
        if (input("Press any key to continue...")):
            exit()
        
    with open(datapath,"r",encoding="utf-8") as f:
        meta = json.load(f)

    if str(datetime.date.today()) == meta["Date"]:
        exit()
    writer = Writer(meta)
    writer.write(script_dir)