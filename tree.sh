# Create project directories
mkdir -p src/{config,entities,systems,ai,maze,world,states,input,rendering,themes,highscore,persistence,audio,cheat}
mkdir -p tests docs/project_management

# Create package init files
touch src/__init__.py
touch src/{config,entities,systems,ai,maze,world,states,input,rendering,themes,highscore,persistence,audio,cheat}/__init__.py

# Create entry files
touch pac-man.py config.json