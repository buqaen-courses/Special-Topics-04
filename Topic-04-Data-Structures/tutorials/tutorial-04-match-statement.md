# Tutorial 4: Match Statement in Python
```bash
Section: Topic-04-Data-Structures — Section 4 (Match Statement)
Level: Beginner
Estimated Time: ~30–35 minutes
Prerequisites: Basic Python, variables, if statements
```
---

## Learning Objectives

By the end of this tutorial you will be able to:

- Understand what the match statement is and when to use it
- Replace if-elif chains with cleaner match expressions
- Handle default cases with `_`
- Use guards (`if` conditions inside cases)
- Match multiple values in a single case
- Use match with functions and type hints

---

## Table of Contents

1. What Is the Match Statement?
2. Basic Match Usage
3. Match with Default Case
4. Matching Multiple Values
5. Guards — Adding Conditions to Cases
6. Match vs If-Elif
7. Functions Using Match
8. Common Beginner Mistakes
9. Practice Exercises
10. Key Takeaways

---

## 1. What Is the Match Statement?

The `match` statement was introduced in Python 3.10. It lets you compare a value against a series of patterns and run code for the first one that matches.

It works similarly to a `switch` statement in other languages, but is more expressive.

Basic structure:

```python
match value:
    case pattern1:
        ## runs if value matches pattern1
    case pattern2:
        ## runs if value matches pattern2
    case _:
        ## default — runs if nothing else matched
```

Key points:

- Python checks cases from top to bottom
- only the first matching case runs
- `_` is the wildcard — it matches anything and is always placed last
- available in Python 3.10 and later

---

#### Mini Exercise

What do you think happens if no case matches and there is no `_`? Nothing — Python simply moves on. Try it mentally with `value = 99` and only `case 1` and `case 2` defined.

---

## 2. Basic Match Usage

#### Matching Numbers

```python
number = 2

match number:
    case 1:
        print("One")
    case 2:
        print("Two")
    case 3:
        print("Three")

## Output: Two
```

#### Matching Strings

```python
color = "red"

match color:
    case "red":
        print("Stop")
    case "yellow":
        print("Wait")
    case "green":
        print("Go")

## Output: Stop
```

#### Matching Booleans

```python
is_logged_in = True

match is_logged_in:
    case True:
        print("Welcome back")
    case False:
        print("Please log in")

## Output: Welcome back
```

---

#### Mini Exercise

Write a match statement that checks a variable `day_number` (1 through 3) and prints `"Monday"`, `"Tuesday"`, or `"Wednesday"`.

---

## 3. Match with Default Case

The `_` pattern is the default case. It matches any value that was not caught by the earlier cases.

```python
value = 5

match value:
    case 1:
        print("One")
    case 2:
        print("Two")
    case _:
        print("Something else")

## Output: Something else
```

Always place `_` last. Python will raise a `SyntaxError` if you put cases after it, since they could never be reached.

#### Default for Strings

```python
fruit = "mango"

match fruit:
    case "apple":
        print("Red fruit")
    case "banana":
        print("Yellow fruit")
    case _:
        print("Unknown fruit")

## Output: Unknown fruit
```

#### Capturing the Unmatched Value

Instead of `_`, you can use a variable name to capture the unmatched value:

```python
command = "quit"

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case other:
        print(f"Unknown command: {other}")

## Output: Unknown command: quit
```

`other` here behaves like `_` but also stores the value so you can use it.

---

#### Mini Exercise

Write a match statement for a variable `status_code`. Handle `200`, `404`, and use a default for everything else.

---

## 4. Matching Multiple Values

You can match several values in a single case using `|` (the OR operator).

```python
day = "saturday"

match day:
    case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
        print("Weekday")
    case "saturday" | "sunday":
        print("Weekend")
    case _:
        print("Unknown day")

## Output: Weekend
```

This is cleaner than repeating the same logic across multiple cases.

#### Matching Multiple Numbers

```python
score = 9

match score:
    case 10 | 9:
        print("A — Excellent")
    case 8:
        print("B — Good")
    case 7:
        print("C — Fair")
    case 6:
        print("D — Poor")
    case _:
        print("F — Fail")

## Output: A — Excellent
```

---

#### Mini Exercise

Write a match statement that prints `"Vowel"` if a variable `letter` is `"a"`, `"e"`, `"i"`, `"o"`, or `"u"`, and `"Consonant"` otherwise.

---

## 5. Guards — Adding Conditions to Cases

A guard is an extra `if` condition added to a case. The case only matches if both the pattern and the guard are true.

```python
match value:
    case pattern if condition:
        ## runs only if pattern matches AND condition is True
```

#### Example — Temperature Check

```python
temperature = 35

match temperature:
    case t if t > 30:
        print("Hot day")
    case t if t > 20:
        print("Warm day")
    case t if t > 10:
        print("Cool day")
    case _:
        print("Cold day")

## Output: Hot day
```

Here `t` captures the value of `temperature` so you can use it in the condition.

#### Example — Weather and Temperature Together

```python
weather = "sunny"
temp = 25

match weather:
    case "sunny" if temp > 20:
        print("Go swimming or have a picnic")
    case "sunny":
        print("Go for a walk in the park")
    case "rainy":
        print("Stay indoors and read a book")
    case "cloudy":
        print("Visit a museum or go shopping")
    case _:
        print("Check the forecast for suggestions")

## Output: Go swimming or have a picnic
```

Notice that `"sunny"` appears twice — the first case has a guard, the second is the fallback for when the guard fails.

---

#### Mini Exercise

Write a match statement for a variable `age`. Print `"Child"` if age is under 13, `"Teen"` if under 18, and `"Adult"` otherwise. Use guards.

---

## 6. Match vs If-Elif

Both do the same job. Match is generally cleaner when you are comparing one value against many fixed options.

#### If-Elif Version

```python
day = "friday"

if day == "monday":
    print("Start of work week")
elif day == "friday":
    print("End of work week")
elif day == "saturday" or day == "sunday":
    print("Weekend")
else:
    print("Midweek")
```

#### Match Version

```python
match day:
    case "monday":
        print("Start of work week")
    case "friday":
        print("End of work week")
    case "saturday" | "sunday":
        print("Weekend")
    case _:
        print("Midweek")
```

#### When to Use Each
```bash
Situation                              Prefer
──────────────────────────────────────────────────────────
Comparing one value to fixed options   match
Complex boolean logic (and/or)         if-elif
Range checks (x > 10 and x < 20)      if-elif
Checking multiple different variables  if-elif
Clean, readable value dispatch         match
```

---

## 7. Functions Using Match

Type hints make it clear what a function expects and returns.

#### Grade Description

```python
def get_grade_description(score: int) -> str:
    """Convert a numeric score to a letter grade."""
    match score // 10:
        case 10 | 9:
            return "A — Excellent"
        case 8:
            return "B — Good"
        case 7:
            return "C — Fair"
        case 6:
            return "D — Poor"
        case _:
            return "F — Fail"

print(get_grade_description(95))   ## A — Excellent
print(get_grade_description(73))   ## C — Fair
print(get_grade_description(40))   ## F — Fail
```

`score // 10` uses integer division to reduce any score to a single digit (e.g. 95 → 9, 80 → 8).

#### Menu Handler

```python
def process_menu_choice(choice: int) -> str:
    """Return the action for a given menu option."""
    match choice:
        case 1:
            return "View profile"
        case 2:
            return "Edit settings"
        case 3:
            return "Show help"
        case 4:
            return "Exit"
        case _:
            return "Invalid choice — please select 1 to 4"

print(process_menu_choice(2))    ## Edit settings
print(process_menu_choice(99))   ## Invalid choice — please select 1 to 4
```

#### Activity Suggester (with Guard)

```python
def suggest_activity(weather: str, temperature: int) -> str:
    """Suggest an activity based on weather and temperature."""
    match weather:
        case "sunny" if temperature > 20:
            return "Go swimming or have a picnic"
        case "sunny":
            return "Go for a walk in the park"
        case "rainy":
            return "Stay indoors and read a book"
        case "cloudy":
            return "Visit a museum or go shopping"
        case _:
            return "Check the forecast for suggestions"

print(suggest_activity("sunny", 25))    ## Go swimming or have a picnic
print(suggest_activity("sunny", 10))    ## Go for a walk in the park
print(suggest_activity("rainy", 15))    ## Stay indoors and read a book
```

---

#### Mini Exercise

Write a function `classify_bmi(bmi: float) -> str` that returns `"Underweight"` for $bmi < 18.5$, `"Normal"` for $bmi < 25$, `"Overweight"` for $bmi < 30$, and `"Obese"` otherwise. Use match with guards.

---

## 8. Common Beginner Mistakes

#### Mistake 1 — Putting cases after `_`

```python
match value:
    case _:
        print("default")
    case 1:          ## SyntaxError — unreachable
        print("One")
```

Fix: always put `_` last.

#### Mistake 2 — Using a variable as a pattern (it captures, not compares)

```python
target = 10

match value:
    case target:     ## this does NOT compare value to target
        print("match")   ## it captures value into target
```

If you want to compare against a variable, use a guard:

```python
match value:
    case v if v == target:
        print("match")
```

#### Mistake 3 — Forgetting Python version

```python
## match requires Python 3.10+
## On older versions you will get a SyntaxError
```

Check your version:

```bash
python --version
```

#### Mistake 4 — Using match when if-elif is clearer

```python
## This is awkward with match
match True:
    case _ if x > 0 and y > 0:
        print("Both positive")
```

For complex boolean logic, stick with if-elif.

#### Mistake 5 — Missing the default case

```python
match status:
    case "active":
        print("Running")
    case "paused":
        print("Paused")
    ## if status is "stopped", nothing happens — silent failure
```

Fix: add `case _` to handle unexpected values explicitly.

---

## 9. Practice Exercises

#### Exercise 1

Write a match statement that checks a variable `number` for values 1, 2, and 3, and prints the word. Use a default for anything else.

#### Exercise 2

Use match to check a variable `day`. Print `"Weekday"` for Monday through Friday, `"Weekend"` for Saturday and Sunday. Use `|` to combine values.

#### Exercise 3

Write a match statement for a variable `status_code`. Handle `200` ("OK"), `404` ("Not Found"), `500` ("Server Error"), and use a default for others.

#### Exercise 4

Write a function `simple_calculator(a: int, b: int, op: str) -> float` that uses match on `op` to handle `"add"`, `"subtract"`, `"multiply"`, and `"divide"`. Return `0.0` for unknown operations.

#### Exercise 5

Write a function `classify_speed(speed: int) -> str` using match with guards:
- $speed \leq 0$: `"Stationary"`
- $speed \leq 30$: `"Slow"`
- $speed \leq 90$: `"Normal"`
- anything higher: `"Fast"`

#### Exercise 6

Write a match statement that checks a variable `letter` and prints `"Vowel"` if it is `a`, `e`, `i`, `o`, or `u`, and `"Consonant"` otherwise.

---

## 10. Key Takeaways

- `match` compares a value against patterns from top to bottom; the first match wins
- `_` is the wildcard default — always place it last
- use a named variable instead of `_` when you need to reference the unmatched value
- `|` combines multiple values into one case
- guards (`if` conditions) add extra logic to a case
- `match` is cleaner than if-elif when comparing one value to many fixed options
- for complex boolean logic or range checks, if-elif is still the right tool
- requires Python 3.10 or later

---

## Quick Reference
```bash
Pattern                  Meaning
──────────────────────────────────────────────────────────
case 1:                  matches exactly 1
case "red":              matches exactly "red"
case 1 | 2 | 3:          matches 1, 2, or 3
case _:                  matches anything (default)
case x:                  matches anything, captures into x
case x if x > 0:         matches if x > 0 (guard)
```