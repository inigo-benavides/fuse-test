# FUSE Risk Management Workflow
A repository for FUSE's Risk Management team.

## Table of Contents
- [Background](#background)
- [Objective](#objective)
- [Installation](#installation)
- [Authors and Contributors](#authors and contributors)
- [Repository Structure](#repository structure)

## Background
Currently, all risk management workflows are separated among each team member's local machines using different programming languages. To allow for common development among team members, there is a need to centralize all data and code. This allows greater transparency and increased efficiency in development.

## Objective
The objective of this repository is to centralize all risk management workflows for common development. We intend to migrate our workflow to a dedicated EC2 instance and use GitHub to manage code development and deployment.

## Installation
The `requirements.txt` lists all the Python dependencies to use this module. It is recommended to use python version 2.7.x as well as have Anaconda installed.
To install depedencies, change directory to this module and run:
```pip install -r requirements.txt```

Since this module also uses packages installed from Anaconda, we'll need to install those dependencies too from `package-list.txt`(for OSX):
```$ conda create --name <env> --file package-list.txt ```

## Authors and Contributors
- Inigo Benavides (@inigo-benavides): Data scientist
- JF Darre: Chief Risk and Analytics Officer
- Diana Yamzon: Data analyst
- Mel Ilagan: Credit Policy
- Benjo Sison: Operational risk

## Repository Structure
- bin: contains essential scripts for minimal functioning of the repository
- creds: contains credentials for various external API usage
- data: contains all relevant data sets
- docs: contains documentation of all work flows
- scripts: contains Python scripts for various workflows

