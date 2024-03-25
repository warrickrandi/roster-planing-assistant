**Roster Planing Assistant**

**Config Changes**
1. Create the .env file and Create the variables

**To Run the Application on Docker**

1. Inside the Project folder run below commands from terminal
```bash
   docker build -t llm-app .
   docker run --name llm-app -d -p 8888:8888 llm-app
```

**Run the Project Locally**
1. Install all required libraries
```bash
   pip install -r requirements.txt
```
2. Run the APP
```bash
   stremlit run app.py
```

**Database has created with sqllite**