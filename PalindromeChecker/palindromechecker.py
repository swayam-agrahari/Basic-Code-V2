class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        l = 0
        r = len(s) - 1
        while l < r:
            if not s[l].isalnum():
                l += 1
            elif not s[r].isalnum():
                r -= 1
            else:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
        return True


sol = Solution()

# Test cases
test_cases = [
    "A man, a plan, a canal: Panama",  
    "race a car",                       
    "No 'x' in Nixon",                 
    "pheonix-official",
    "#!@#%@,.,..",
    " "
]

for i, test in enumerate(test_cases, 1):
    result = sol.isPalindrome(test)
    print(f"Test case {i}: {repr(test)} → {result}")
