# Task list manager

Run the script in the general form
```
python3 tasks.py COMMAND DATA_NEEDED_BY_COMMAND
```

## Add a task

```
python3 tasks.py add "Fold the laundry"
```

## List tasks

Print a sequence of TASKID, DESC pairs for the tasks in the database.

To list just the outstanding tasks:
```
python3 tasks.py list
```

To also include the ones marked as completed:
```
python3 tasks.py list all
```


## Mark task as complete

```
python3 tasks.py done TASKID
```

## Delete a task

```
python3 tasks.py delete TASKID
```
