```
 $$$$$$\                      $$\   $$\                                   
$$  __$$\                     $$$\  $$ |                                  
$$ /  $$ | $$$$$$\   $$$$$$\  $$$$\ $$ | $$$$$$\  $$$$$$\$$$$\   $$$$$$\  
$$$$$$$$ |$$  __$$\ $$  __$$\ $$ $$\$$ | \____$$\ $$  _$$  _$$\ $$  __$$\ 
$$  __$$ |$$ /  $$ |$$ /  $$ |$$ \$$$$ | $$$$$$$ |$$ / $$ / $$ |$$$$$$$$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |$$  __$$ |$$ | $$ | $$ |$$   ____|
$$ |  $$ |$$$$$$$  |$$$$$$$  |$$ | \$$ |\$$$$$$$ |$$ | $$ | $$ |\$$$$$$$\ 
\__|  \__|$$  ____/ $$  ____/ \__|  \__| \_______|\__| \__| \__| \_______|
          $$ |      $$ |                                                  
          $$ |      $$ |                                                  
          \__|      \__|                                                  
```

<p align="center">
    <em>Mini App Description</em>
</p>

<p align="center">
<a href="" target="_blank">
    <img src=
    "https://img.shields.io/badge/>=3.12,<4.0-2596be?style=flat&logo=Python&logoColor=white&label=Python&labelColor=gray"
    alt="Supported Python versions">
</a>
<a href="" target="_blank">
    <img src=
    "https://img.shields.io/badge/0.00%25-red?style=flat&logo=checkmarx&logoColor=white&label=Coverage&labelColor=gray"
    alt="Coverage">
</a>

</p>

# Develop Checklist

1 - Take a issue for you in [Issues](https://github.com/Automalogica/SunOp-data-processor/issues)

2 - Create a branch named **issue_XXX** from [main](https://github.com/Automalogica/SunOp-data-processor/tree/main)

3 - [Create your env and install the dependencies ](#create-venv)

4 - Make your modifications

5 - [Test your modifications](#test)

6 - Ensure 100% of [Coverage Report](#coverage-report)

7 - Create a PR from your **issue_XXX** to **main**

8 - Request revision from a tech leader

9 - If denied return to step 4

10 - If accepted merge the **issue_XXX** then delete this branch

11 - Auto deploy action will be triggered

# Create venv

```bash
python3.12 -m venv venv

source ./venv/bin/activate

pip install poetry

poetry install
```

# Test
```bash
docker compose up -d

tox

docker compose down
```
### All tests must be passed
<img src=
    "https://i.imgur.com/xQGH83l.png"
    alt="Teste">

# Coverage Report
```bash
OPEN DataProcessor/.tox/report/index.html
```
### Must be 100%
<img src=
    "https://i.imgur.com/Hj9tJ73.png"
    alt="Coverage">

