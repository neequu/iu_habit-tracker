# Habit Tracker CLI  
*A simple command-line tool to build and analyze habits*  

**What this does**  
Track daily/weekly habits, mark completions, and get analytics on your streaks—all from the terminal. Built with Python + SQLite.  

---

## Quick Start  

### 1. Clone & Enter  
```bash
git clone https://github.com/neequu/iu_habit-tracker.git
cd habit-tracker
```

### 2. Install Dependencies  
```bash
pip install -e .[dev]  # Installs the app + dev tools (pytest)
```

### 3. Run It 
```bash
# Use the launcher script (make it executable first)
chmod +x habit
./habit --help

# Or directly via Python
python -m src.app --help
```

---

## Command Reference

### **Get Info on Any Command**
This lists the arguments and options for a given command
```bash
./habit COMMAND_NAME --help # Use this --help flag

# Examples:
./habit delete --help
# or
./habit complete --help
```

### **Habit Management**
```bash
# Create a new habit
./habit create NAME 
  --periodicity [daily|weekly|biweekly] # Required
  [--description TEXT] # Optional
  [--start-date YYYY-MM-DD] # Optional. Default is today

# Delete a habit
./habit delete HABIT_ID

# Mark completion
./habit complete HABIT_ID 
```

### **Analytics**
```bash
# List all habits
./habit list-all

# Filter habits by period
./habit list-by-period --period [daily|weekly|biweekly]

# Get streaks
./habit streaks

# Check longest streak for a habit
./habit longest-streak HABIT_ID
```

---

**Example Session:**
```bash
1. ./habit create "Meditate" --periodicity daily
2. ./habit complete 1
3. ./habit list-by-period --period daily
4. ./habit longest-streak 1
```
---

## Project Info  

### Project Structure  
```markdown
src/
├── cli/          # Command definitions
├── core/         # Business logic (tracker, analytics)
├── infra/        # Database & utilities
└── app.py        # Entry point
```

### Running Tests  
```bash
pytest -v
```
or
```bash
pytest tests/ -v
```

### Debugging Tips  
- The SQLite DB is at `src/infra/habits.db` (use `sqlite3` to inspect it).  


---

## FAQ  
**Q: Why do I need to `chmod +x habit`?**  
A: It makes the `habit` script executable (Linux/Mac quirk). Windows users can use `python -m src.app` instead.  

**Q: How do I reset everything?**  
A: Delete `src/infra/habits.db`—it auto-creates on restart.  

---
Made for DLBDSOOFPP01 Object Oriented and Functional Programming with Python  @ IU University of Applied Sciences.  
 