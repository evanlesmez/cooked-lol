# Cooked League of Legends

A place to analyze data about champions to come up with strategies and build ideas.  
Main data sources are:  

- [lolalytics](https://lolalytics.com/lol) for global game data statistics.  
- [LoL.fandom Wiki](https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki) for champion data.  
- [Riot API](https://developer.riotgames.com/apis) eventually for the most up to date info.  

## Quickstart

You will need Jupyter Lab installed or a text editor capable of editing Jupyter Notebooks.  

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements/core.txt
pip install -r requirements/dev.txt
python3 -m ipykernel install --user --name lol-cooked --display-name "Python lol-cooked"
# launch with project as PYTHONPATH
scripts/jupyter_lab_w_path.sh
```

## Rendering Jupyter notebooks to static formats

Install [Quarto](https://quarto.org/).  
Make sure to include a raw YAML block heading in the notebook like:  

```yaml
title: "example title"
# optional formatting 
format: 
  html:
    code-fold: false
jupyter: python3
```

Then use [`quarto render --to [fmt] [path/filename]`](https://quarto.org/docs/get-started/hello/jupyter.html#rendering)  
