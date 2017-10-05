# CSE 132 Code Plagiarism Detection Scripts

Created for CSE 132 at Washington University in St. Louis. This will pull repositories from a Github organization and send files to MOSS.

## Requirements

* Python 2.7 or 3

## Initial Setup

Copy repoauth.py.example into repoauth.py and replace the username and password strings.

Run

```shell
    python repositories/repo-grabber.py assignment-2
```

to clone all the repositories for `assignment-2` into the `repositories/assigment-2` folder.

## Sending requests to MOSS

Run

```shell
    python cpds.py [old-files-substring] [new-files-substring]
```

For example, running

```shell
    python cpds.py module2 spring2016-module2
```

will compare all files in folders with the substring "module2" in their name, with all files in folders with the substring "spring2016-module2" in their name. This will compare all Module 2 folders from the Spring 2016 semester with any Module 2 folder, from the current semester and from previous semesters.

## Author

Evan Simkowitz, modified from a solution by Brian Lam

Washington University in St. Louis

