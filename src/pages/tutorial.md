# Problems
### Problem Page
After the tutorial page, you will be taken to the <Problem Page>. This is the page where you manage the current problems that you are adding asset tests for. To add a problem, simply click the plus button, enter the PM number into the popup, and select 'Add'. This will add the problem to the problem dashboard, and the program will find any open jobs and display them to you.

To add tests, click the 'Enter' button on the right of the problem, and you will be taken to the <Test Page>. Click the 'Delete' button on the right of the problem to remove it from the dashboard.

### Adding Tests and Jobs
When you add tests into a problem through the <Test Page>, the problem will keep track of how many tests you've added, and it will automatically sort these based on scripts. This way, on the dashboard in the <Problem Page>, it can display a summary of the currently tested items.

In the same way, any jobs raised are also shown on the dashboard with their asset numbers and descriptions. For any tests that have jobs raised and have the "Pass W/C" result, since this means the job was not finished, the dashboard will show any parts that are required for these jobs if the part information is given in the job. More on parts and jobs in later sections.

### Syncing
You'll notice that when you add tests and jobs and then navigate back to the problem dashboard, they will be shown in blue with plus signs. This indicates that these are *unsynced*. This will help you determine what has been done since the last sync to avoid confusion.

To sync, click the 'Sync' button on the top of the problem dashboard. This will bring up a popup window that will do pre-sync checks, currently for each problem open in the dashboard, it will display any assets that have more than one test assigned to it and/or more than one job raised. This is a last resort to ensure that you haven't accidentally doubled up testing or added two jobs instead of one, etc. Most of the time, these duplicates aren't actually issues, i.e., testing an asset normally but also completing a Class I or II test or having two different issues requiring jobs for an asset.

The script information for tests and job descriptions for jobs will be displayed with any double ups that have been found. Once you have confirmed that no unwanted double ups have occurred, click the 'Sync' button to start the syncing process.

The popup will close and bring you back to the problem dashboard where all of the previously blue tests and jobs will now be black and have no plus signs next to them.

# Testing
### Assets and Script Matching
To test an asset, navigate to the <Test Page> by clicking the 'Enter' button to the right of any problem on the <Problem Page>. Once there, simply enter the asset number into the field and press enter.

The program will look up this asset. Once found, it will grab all of the asset information. Using the asset information, the program will attempt to match it with the stored scripts that it has. If it finds a match, it will automatically select this and display it to you. Otherwise, it will ask you to select it from the available options. You can override this automatic script matching by entering the asset number and then clicking the 'Choose' button.

Just below the asset number field, you will see the item's summary (number, model, manufacturer, etc.). This line also contains the asset's last updated time. Ensure to check this to ensure you or someone else haven't already tested this item. There is also a field with the item's current room in it. Edit this and press the 'Save' button to the right of it (or just save the test), and the asset's room will be updated. Just below the asset field is a brief reminder of the problem that you are in. Then we get to the main script / test section.

### Scripts
On the right displayed is the script lines along with their *default values*. You will see with some scripts they will have their script line text in red, indicating that this field is free text but still required.

The default values, whether a free text line is required or not and more are editable. To edit, delete or add scripts, navigate to the <Settings Page> by going back to the problem dashboard and clicking the 'Settings' button, then click 'Manage Scripts'. This will show you all currently available scripts.

To add a script, click the '+' button in the top right corner. Enter the script number (or description) of the script you want to add, the tester number that you use for the script, and a nickname and then select 'Go'. If the script number already exists, you will be notified. Otherwise, the program will find the script and display to you its script lines.

Go through each script line and add the default value for each line and tick the required box on free text lines that are required.

Persistence of a script line means that if you change this script value from the default during testing of an asset, the program will persist this value for assets of the same model (using the same script). For example, if my default value for the first script line of a bed script was "Pass", and I went and tested an FL250 bed with this script, changed that line to "N/A" and saved the test, if the persistence box is ticked on the script for that line, for all future FL250 beds that I test, the first script line will default to "N/A". In this way, the program will *learn* the differences between script line answers for items of different models.

Condition lines are also present in some scripts; these are required free text fields that will default to '1'. Ensure that the condition line is ticked if your new script has one and that it is required and non-persistent.

Once you are happy with the state of the *default* script, click 'Save Script' to add that script into the program. You will now be able to test assets under with that script, and the program can look for the nickname of the script in the asset description to try and automatically select it for you. If you aren't sure about default values or persistence, don't worry; these are always changeable when actually testing and aren't for any other purpose other than convenience.

To edit or view a script, simply click the 'Edit' button on the right of any script. This will show the same popup you see when adding a script except the script number, tester number, and nickname are already filled in. Make your edits, click 'Save Script,' and the edited script is ready to go.

Back to testing, when you have entered an asset and the script has been found, another field will show up in the middle with the tester number for the script. This can also be changed for the test; however, it won't be saved permanently to the script. To permanently save a new tester number, just edit the script as described above.

### Adding Jobs
To add a job to a test, simply click the 'Add Job' button. This will bring a popup with department and contact names pre-filled; feel free to edit these if they are incorrect. Then enter the job's comment in the

 bigger text box.

If you are adding parts to a job, either that you've used them or require them, enter the item number in the right side field below the comment box and the quantity in the box on the left side. Once you enter a part number and click away from the field, the program will search for the part and display to you its description or a short message indicating that it couldn't be found to ensure that you have entered the correct number. To add more than one part, click the '+' button on the right side near the bottom to add another set of part number / quantity fields. If you add too many of these or don't need to add parts at all, don't worry; any blank part number / quantity field sets will be ignored when creating the job. The 'Search' button in this popup and more about parts will be discussed in the next section.

Once you have finalized the job details, click save at the bottom of the popup. The program will automatically enter the job's comment into the overall test comment for convenience. To delete a job you have raised, click the 'X' button that shows up when you have added a job; this will delete the last added job for this asset.

### Parts
As you could probably tell, this program gives the basics to allow for searching for parts. By clicking the 'Search' button on any job you are about to raise or by navigating to the <Settings Page> and then clicking 'Search Parts,' you are shown two main things. Fields with values that you can use to search for parts and a list of the parts sorted in most-recently-used order. This way, any parts that you use often will show up first in case you need to check their part numbers.

If you have entered this page through the raising of a job, you will see a 'Go' button next to each part; clicking this button will autofill the part number into the part number field of the job popup.

To search for a part, simply enter in some search terms for however many fields you like, and then click the 'Search' button. The search for each field looks for the values you enter in any part of the field for that part (case insensitive). For example, typing "molift" into the part description field will look for any parts that have "molift" in their part description; typing "actuator" into the part description field and "aidacre" into the manufacturer field will look for any parts that have "actuator" in their part description AND have the text "aidacare" in their listed manufacturer. Be careful with broad searches as they may take a few seconds to load all of the possible parts.

### Saving the Test
Once all of the script, job, part, and room information is correct, select the test result from the options (hover over them to see more detail) and then press 'Save'. This will run a bunch of checks to ensure that this test is correct and makes sense; these checks include:

- Making sure that if a job is raised or any script line is failed that a comment is provided and an appropriate result selected
- Confirm with you of the asset location if the test is "Pass W/C" and there is a job, to ensure the asset's location is up to date in case the job is reassigned
- Check any required fields to make sure they are filled in
- Ensure that the sync is not currently running to avoid database lock issues
- More that will show popups to you if things go wrong

### Editing / Removing a Test
Once you have added a test for an asset, you will notice that the asset number is saved in the asset number field of the <Test Page> and now the 'Edit' button has become available.

This button becomes available whenever you enter an asset number that has been tested already (ensure you add appropriate suffixes to asset number to see this button show up). Clicking the edit button opens up exactly what you see when you add a test, except all of the values are the values of that test. Make your edits and click 'Save' again to edit the test or press 'Remove' to remove the test altogether. Removing the test removes all data associated with the test, including any jobs raised.