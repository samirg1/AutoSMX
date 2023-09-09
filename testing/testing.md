# UI and UX Testing

### Test Details

| Last done | Result |
| ----------- | ----------- |
| beta v1.7.0 | pass |
| v1.0.0 | some fails |
| v1.0.1 | pass |

---

### Tutorial Page

1. Open page and scroll through and ensure it all looks right.
2. Click the *Skip* button that takes you to either the *Calibration Page* or the *Test Page*.
3. Ensure that
    - In storage `"tutorial_complete": true`

###
---

### Calibration

1. Go to the *Calibration Page*
2. Click open each *?* box and view contents
3. Click on each button and click the top left corner
4. Once completed ensure
    - The page has been changed to the *Test Page*
    - All values in storage under `"positions"` have been set to low values (close to `[0, 0]`)
    - In storage `"calibrated": true`

###
---

### Scripts and Results

1. Go to the *Test Page*
2. Input item number then select *Choose*
3. For each script that shows up
    1. Select it
    2. Check that it shows up properly and all fields are correct
    3. Alternate with turning capslock on / off
    3. Ensure default values are correct
    4. Change some of the default values
    5. Choose one of the final results
    6. Press *Save*
    7. Then ensure that
        - The script is selected properly
        - All fields are inputted correctly and in the right case
        - The correct final result is shown


###
---

### Test-Jobs and Comments

1. Enter an item number and choose a script
2. Add 3 random jobs to the test, one with a part number
3. Ensure that
    - The *X* button shows up to delete a job
    - The number of jobs displays correctly (*Add Job(3)*)
    - The test comment is updated with each job separated by a newline
4. Delete a job and ensure that the previous points are updated accordingly
5. Add back a third job and save the test
6. Ensure that
    - Each job is entered correctly and saved
    - The final comment is entered into its box correctly

###
---

### Script and Location Matching

1. Enter a valid item number and press *Go*
2. Press *Cancel* to ensure that the page resets with the same item number before pressing *Go* again
2. Ensure the program goes to the *Asset Tab* and takes all the information in before cancelling the asset edit
3. Ensure the program matches the correct script to the item (the exact matching is tested automatically)
4. Attempt to add a job and ensure that the contact name and department have been auto-filled, don't add the job
5. Press *Save*
6. Ensure the previous item number is saved
6. Go to the *Job Page* and ensure that there is a job there that matches the item's location information
7. Enter an item number that has a description that cannot be identified by the program
8. Ensure that all previous checks are true and that the script selection popup appears and selects the script properly

###
---

### Jobs

1. Enter and save a test for items with test-jobs
2. Navigate to the *Job Page*
3. Ensure that the job is clearly displayed as well as its tests and raised jobs
4. Click the *+* button and enter a previous item number and save the test
5. Ensure that 
    - the program looked for the location details in the asset tab
    - a second job was not added (as it would be the same as the previous one)
6. Click the *Enter Job* button whilst selecting the main job, and all of its tree children and enter another item number
7. Ensure that for each instance
    - the program did not look for location details
    - there is still only one job displayed in *Job Page*
    - the testing and jobs raised updates correctly
8. Click the *+* button and enter in a new item number from a new job
9. Ensure that
    - the program looks for location details
    - a second job pops up and is displayed correctly
10. Add 3 more jobs this way
11. Delete each job by selecting a different child / parent node each time and then click the *Delete Job* button
12. Ensure that
    - Each deletion causes the relevant updates to occur on the page
    - The page is now empty with the default message being shown
    - The *Delete Job* and *Enter Job* buttons are disabled
13. Click on the *Tutorial* and *Calibrate* buttons and ensure they take you to the respective pages and set the respective attributes in storage to false

###
---

### Failsafe 

1. Enter an item number and press *Go*
2. Immediately activate the failsafe by moving the mouse to any corner of the screen
3. Ensure that 
    - The failsafe activation popup is opened
    - The page is reset with the same item number still in the field
4. Enter an item number, wait for the script to match, add a test-job and then press save
5. Activate the failsafe
6. Ensure that
    - The failsafe activation popup is opened
    - The page is again reset with the same item number still in the field
    - The test and any test-jobs raised were not saved by the program by viewing the job page and storage if needed

###
---

### Item Model Script Updating

1. Enter an item number that has a valid model (not blank or a copy of its description)
2. Change the default script values dramatically before saving
3. Check that that item model is now in stored with the dramatically different script values in storage
4. Enter the same item number in, ensure that the new 'default' values are the dramatically different ones that were in storage
5. Change the script values back to the old default values and then save
6. Ensure that
    - The item model has now been removed from storage
    - Entering the item in again gives the old default script values

###
---

### Test Editing

1. Attempt to edit an item with no job currently available, ensure it fails
1. Enter an item and run a normal test on it
2. Enter the same item and attempt to edit the test, ensure that
    - The script is not looked up but found
    - The details show up the same before
    - Changing the values and pressing save changes the values in the test successfully

###
---


