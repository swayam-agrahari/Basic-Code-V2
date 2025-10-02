# **Palindrome Checker Overview**

This Python script defines a class `Solution` with a method `isPalindrome` that checks whether a given string is a **palindrome**, ignoring:

- Case sensitivity (uppercase vs lowercase)
- Non-alphanumeric characters (spaces, punctuation, symbols)

---

## **How It Works**

```python
s = s.lower()
```

- Converts the entire string to lowercase to make comparison case-insensitive.

---

```python
l = 0
r = len(s) - 1
```

- Initializes two pointers:

  - `l` starts from the beginning (left)
  - `r` starts from the end (right)

---

```python
while l < r:
```

- Loop continues as long as the `left` pointer is before the `right` pointer.

---

```python
if not s[l].isalnum():
    l += 1
```

- If the character at the left pointer is **not a letter or number**, skip it by moving `l` forward.

---

```python
elif not s[r].isalnum():
    r -= 1
```

- If the character at the right pointer is **not a letter or number**, skip it by moving `r` backward.

---

```python
else:
    if s[l] != s[r]:
        return False
    l += 1
    r -= 1
```

- If both characters are alphanumeric, compare them.

  - If they **don’t match**, return `False` (not a palindrome).
  - If they **match**, move both pointers closer and keep checking.

---

```python
return True
```

- If the loop finishes without returning `False`, it means all characters matched → the string **is a palindrome**.

---

### **Example Output:**

For the test case `"A man, a plan, a canal: Panama"`:

- After removing non-alphanumeric characters and lowercasing, it becomes:
  `"amanaplanacanalpanama"`
- The string reads the same forward and backward → returns `True`.

---

### **Test Cases in the Script**

```python
test_cases = [
    "A man, a plan, a canal: Panama",
    "race a car",
    "No 'x' in Nixon",
    "pheonix-official",
    "#!@#%@,.,..",
    " "
]
```

#### Output:

```
Test case 1: 'A man, a plan, a canal: Panama' → True
Test case 2: 'race a car' → False
Test case 3: "No 'x' in Nixon" → True
Test case 4: 'pheonix-official' → False
Test case 5: '#!@#%@,.,..' → True
Test case 6: ' ' → True
```

## Summary

- **Efficient two-pointer approach**
- **Handles letters, numbers, spaces, punctuation**
- Great for checking palindromes in both words and sentences

---
