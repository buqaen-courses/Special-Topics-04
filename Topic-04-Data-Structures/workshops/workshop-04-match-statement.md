# Workshop 4: Match Statement

**Section**: 9 - Match Statement (30 min)
**Level**: Beginner
**Prerequisites**: Tutorial 4 (Match Statement)

---

## 🎯 Workshop Objectives

By the end of this workshop, you will:

1. **Use match statement** for value checking
2. **Replace if-elif chains** with match
3. **Handle default cases** in match

---

## 📋 Workshop Structure

1. [Setup](#setup)
2. [Exercise 1: Basic Match](#exercise-1-basic-match)
3. [Exercise 2: Match with Default](#exercise-2-match-with-default)
4. [Exercise 3: Match Applications](#exercise-3-match-applications)

---

## 🛠️ Setup

Create a new Python file called `workshop_match.py` for your exercises.

---

## 🏃 Exercise 1: Basic Match

### Task 1.1: Number Matching
Create a match statement that checks if a number is 1, 2, or 3 and prints the word.

```python
# TODO: Match numbers 1, 2, 3
number = 2
match number:
    # Add your cases here
```

### Task 1.2: Color Matching
Use match to check colors "red", "blue", "green" and print what they mean.

```python
# TODO: Match colors
color = "red"
match color:
    # Add your cases here
```

### Task 1.3: Day Matching
Create match for days of the week to check "monday", "tuesday", "wednesday".

```python
# TODO: Match days
day = "monday"
match day:
    # Add your cases here
```

---

## 🏃 Exercise 2: Match with Default

### Task 2.1: Default Case
Create match with specific cases for 1, 2, 3 and default for others.

```python
# TODO: Match with default case
value = 5
match value:
    case 1:
        print("One")
    case 2:
        print("Two")
    case 3:
        print("Three")
    case _:  # Default case
        print("Other number")
```

### Task 2.2: Fruit Matching with Default
Match fruits "apple", "banana", "orange" with default for other fruits.

```python
# TODO: Match fruits with default
fruit = "grape"
match fruit:
    # Add your cases here
```

### Task 2.3: Grade Matching
Create match for grades "A", "B", "C", "D" with default for "F".

```python
# TODO: Match grades
grade = "B"
match grade:
    # Add your cases here
```

---

## 🏃 Exercise 3: Match Applications

### Task 3.1: Calculator Operation
Use match to check operation "add", "subtract", "multiply" and print what it does.

```python
# TODO: Match calculator operations
operation = "add"
match operation:
    # Add your cases here
```

### Task 3.2: Traffic Light
Create match for traffic lights "red", "yellow", "green" with appropriate actions.

```python
# TODO: Match traffic lights
light = "red"
match light:
    # Add your cases here
```

### Task 3.3: Menu Selection
Use match for menu choices 1, 2, 3, 4 with default for invalid choices.

```python
def handle_menu(choice: int) -> str:
    # TODO: Match menu choices
    match choice:
        case 1:
            return "View profile"
        case 2:
            return "Edit settings"
        case 3:
            return "Help"
        case 4:
            return "Exit"
        case _:
            return "Invalid choice"

# Test your function
print(handle_menu(2))  # Should print "Edit settings"
print(handle_menu(5))  # Should print "Invalid choice"
```

### Task 3.4: Weather Response
Create match for weather "sunny", "rainy", "cloudy" with appropriate responses.

```python
# TODO: Match weather conditions
weather = "sunny"
match weather:
    # Add your cases here
```

---

**Workshop Version**: 4.0 - Simplified
**Last Updated**: February 2026
**Estimated Time**: 30 minutes