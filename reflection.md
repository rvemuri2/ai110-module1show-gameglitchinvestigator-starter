# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- ## What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  - The first bug I noticed were the attempts, it says attempts left: 7 under Make a guess. However, attempts allowed: 8 is what is written below the difficulty on the left.
  - Pressing enter after I gave an input does not do anything, I believe this is a bug because in the input, it does say "Enter to apply"
  - I noticed that there was something weird with the difficulties. Hard has a range of 1-50, while normal has a range of 1-100. It should have been the opposite, because the longer the range of numbers, the harder it should be to guess that number.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

1. Input: 8, Expected Behavior: The attempts left count should have been lowered by 1, and the history should have updated. Actual behavior: The hint was given, but history and attempts were not updated.

2. Input: 0, Expected behavior: Should have given me a go higher hint or an out of range error. Actual behavior: Updated previous history of input of 8 and attempts lowered by 1. The hint says to go lower instead of higher. Console Output/Error: No error given by the actual code, but should have been out of bounds or out of range error. No actual error given by console.

3. Input: 20, Expected behavior: A hint that says either I am too high or too low, or I got the number right, with the attempts left subtracting by 1. Actual behavior: The hint didn't show up and the attempts left didn't subtract by 1. What I am understanding is that sometimes the game is glitchy in terms of when the hints show up after an input of 0. There can be a delay of when the history takes in the input. Console Output/Error: None from the output, no real errors, just doesn't execute as planned

4. Input: 15, Expected behavior: A hint that says either I am too high or too low, or I got the number right, with the attempts left subtracting by 1. Actual behavior: The history says I repeated my guess of 20, which I did not do. My score goes from 0 to -5, which I didn't realize before. The guess does say to go lower, but there's a bad bug in the history. Console Output/Error: History should not have repeated that 20 input.

5. Input: 7, Expected behavior: Either to get the number right or to higher. I had hit the number of attempts, so I expected the attempts to end and give the alert of "Out of Attempts!" And give a number between 8 and 20. Actual behavior: It says to go lower, even though when at 8, it said to go higher, and I found the number was 71. Console Output / Error: It gives the wrong hints as the number was above 20. It should have told me to guess higher every time according to the inputs I gave. No actual error given by the console

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
| ----- | ----------------- | --------------- | ---------------------- |
|       |                   |                 |                        |
|       |                   |                 |                        |
|       |                   |                 |                        |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code AI tool for this project
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - One example in which the AI suggestion that was correct was when it said that there was no range validation in parse_guess function. This is correct because I was able to enter 0 as an input, which resulted in a hint that was incorrect. There should have been logic to check if the input is in the range of the difficulty set.I verified this result by inputting in parameters and returned an error/alert if the input is out of the range of the parameters.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - One example of the AI suggestion that I thought was incorrect or misleading was when reviewing the error for the range validation, the AI never once mentioned the other half of that error. It never mentioned to fix or to evaluate the number of attempts that would decrease even with an invalid number guess. In testing, I found the number of attempts to be decreasing, even when I guessed a number that is too low or high for the range and when it gave me an alert saying so. This allowed me to think for myself and adjust the code accordingly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I decided that a bug was really fixed by testing all the edge cases of the feature manually and then also making a test case for it in test_game_logic.py. I had to test over and over again depending on the bug, but the most important thing was to come up with a list of edge cases. That way, there won't be anything missed in the testing and then having similar cases in the testing code makes it reliable.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - One test I ran manually was seeing how the history is updating in real time after the user attempts a valid guess. The bug was actually how I was ordering the code, and that I needed to move some sections of the code. I learned that Streamlit re runs the script top to bottom on every click, and in app.py, initially, the history, score, and attempts were rendered before the submit handler running, so UI draws old values, so it needed to be moved.
- Did AI help you design or understand any tests? How?
  - Yeah, the AI helped me to design the tests, and understand that some existing tests were not working properly. In the code, check_guess returns a tuple, but the initial test asserted a result with just a string. So, the AI helped me to catch that with the updated code, so that test was able to be modified correctly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - So, I learned how Streamlit "reruns" in that every time the user interacts with the application, Streamlit re-runs the entire Python script from top to bottom. In a normal app, there is no event handler system. In Streamlit, the whole script just runs again. So, that means that variables are reset and so that would mean scores would go back to 0 each time. That's why we have session states, so that there is a dictionary that survives in the re-runs, and the data is not lost even if the re run happens.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  - I think one habit or strategy I would use from this project in future labs or projects is taking time to go through all the edge cases of testing (in this case manually) before I start to even look at the code. I think looking at logs and understanding errors is critical for any developer. I want to get in the habit of Test driven development (TDD) as that is the best way to diagnose problems and efficiently solve problems.

- What is one thing you would do differently next time you work with AI on a coding task?
  - Next time, I should not just tell the AI to refactor the entire file, rather focus on individual pieces and then test individual piece/section. I know that this is slower to test, but would be more accurate. In this project, the code was simple, but next time the project could be more complex. It would be also easier to follow for me, the developer, and it is easier to be able to fix any mistakes.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - The project really changed how I see the quality of code the AI has generated in that the AI has been very accurate and even thinks of test cases that may have missed my eye. The AI is also really good at documentation in explaining the changes and why that change should be there.
