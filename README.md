This is a Python script to automatically generate daily report for Obisdian users. It can find all task items in the target directory and store data in the `data.json` file. 

# Usage

## Start to use

Of course the first thing to do is clone the repo to your local directory and enter the directory in command block.

Then install the dependencies by running the following code.

```
pip install -r requirements.txt
```

Initially, the storage file `data.json` is not created. You need to fill in the `config.yml` and run the script. The `config.yml` is as follows:

```yml
Config:
  VaultPath: "" # The path to your target Obsidian vault
  TaskDir: ""  # The relative path to the directory containing task files in your vault
  FileToExclude: [] # Files you don't want the script to analyze in TaskDir
  ReportPath: "" # The relative path to the file storing daily report in your vault
``` 

Before fill in the file, first organize the files in your vault. The script only analyze files in the `TaskDir` and exclude files in `FileToExclude`. It finds all task lines start with `- [ ]` or `- [x]`. So you may create task files specifically containing tasks in the `TaskDir` directory. The plugin [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) is recommanded.

After filling in the `config.yml`, run the script to generate initial `data.json` file.

```
python main.py
```

The script will generate a `data.json` file while not adding lines to your report file. It will store the current state of your tasks. The next day you run the script, it will automatically analyze changes, generate report according to the template and add it to your report file.

## Daily usage

After the initialization, the rest usage can be fully automatic. You just need to run the script every day and it will automatically does everything for you. In other words, today you run the script and it generates your daily report yesterday. It will work only once every day since it records the date.

In the template there is a {remark} blank. If you want to say something, just use the Diary core plugin in Obsidian and store the file in the vault's root path. The script will copy the content into your report and delete the diary file. You need to ensure the diary file must name by `YYYY-MM-DD`, in other words, the initial setting of the core plugin.

For now, the remained tasks displayed in template are random 5 or less tasks unsorted. This feature is in future developing plan.

# Develop Plan

I will improve the script according to issues. In the future, I may add features like:

- DIY template
- Tag analysis
- AI comment on your day
- Sort your remaining tasks
- ...

Please give me feedback by issues.


# Tips

You can add the script to your start menu and your computer can automatically run it when it starts. For different operating systems, the solution can differ. You may explore yourself.