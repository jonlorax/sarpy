If you have content you would like to contribute or found a typo, please follow these procedures.

1. If you are a Developer on this project, skip to 2. If you are not a Developer on this project, fork this project to your personal account.
2. Create a new [feature branch](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) from the `master` branch
3. Add desired contributions/corrections to your feature branch
4. Create a Merge Request (MR) from your feature branch to the `dev` branch of this project.
5. The dev team will be notified of your request to contribute and begin a code review with you as needed to accept your feature branch
6. Be on the lookout within your merge request for code review comments from the Code Owners needing your feedback inline under your Pull / Merge Request (PR/MR) `Changes` section
7. Once all of your PR/MR threads have been resolved, the code owners will approve the merge request and your code will be added to the codebase for the next release.

- If you have a time sensitive need or don't see progress on your MR within a week, please contact the CODEOWNERS.

## Example

### Scenario: 
Bug #1 has been reported for our application. 

### Resolution:
1. Fork the original project into your personal repository.
2. Create a feature branch named fb_bug1 from master in a command line:
```
git clone <your project>
git checkout master
git branch fb_bug1
```
3. Make your fixes in fb_bug1
4. Sync the master branch in your fork with the master branch in the original project.
5. Merge your code from fb_bug1 into dev
```
git checkout master
git branch dev
git checkout dev
git merge gb_bug1
```
* This step is very important because other changes might have happened in master
since fb_bug1 was created
6. Create a pull request from your dev branch into the dev branch in the original project.
7. Respond to threads as necessary.
8. Contributor's role is complete. Owners / Maintainers please go to PUBLISHING.md.
