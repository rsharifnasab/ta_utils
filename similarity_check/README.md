# Local similarity check
What if we want to do similarity check offline and fast? The MOSS is not a good option because it is hard to use, and we can only use it we send codes to server.



### Jplag

Jplag is a local java project which checks source codes for similarity like MOSS, but it's programming interface is not good.



## Wrapper Scripts

There are two wrapper scripts for Jplag which you can use based on your needs. 

### one question
If you only and only have one question to check, then you can use this. the other script is using this script internally too!. 

```bash
./one_question.sh sources/ result/ cpp ./lib.zip
```
the arguments are:
1. The Root folder for submissions.
2. The root folder for writing result. This folder is deleted and re-created before writing, so be careful.
3. Your codes languages (select CPP for both c and CPP submissions)
4. If you provided some basic or library code which all students are using, then you should put it in this `lib` library, so the engine would exclude from similarity results. 

Note: The lib option should point to a zip file which you uploaded for students, not a single folder

### run
if you have more than one question to check, you can use this script instead of manually calling the other script multiple times.

```bash

./run.sh java sources/ result/ ./libs
# or ignore the last parameter if you don't have libs

```

Note: sources codes could be in zip files or single files, the script unzip them automatically (if needed)

## python scripts

There are two python scripts in this project, you don't need them directly. They are responsible for changing student IDs with actual student names which would help the readability.

Although for the correct use, you should place a file named `students.txt` near the wrapper scripts.
The structure should be like this:
```
first name 1 last name 1 972431234
another name and last name 982434567

```

