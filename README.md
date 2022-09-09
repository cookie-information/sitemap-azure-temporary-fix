# A Temporary sitemap workaround 

### What does it do?

Currently, sitemaps are not scannable (due to the structure of XML). However, converting the locations (<loc>) into regular HTML <a> tags solves the issue.

### How does it work exactly?

When putting this together, there were a few things I wanted to ensure:

- All <loc> links must be retrieved
- These <loc> tags must then be replaced with <a> tags
- This list of links must then be saved as as HTML file and hosted somewhere accessible
- There should be no need to manually do any work after set-up - a cron job will set the task off on its own and replace the old html file with the newest list

This meant that I settled on an Azure function (which you can find in the FrequencyTimer folder) that runs the Python function that goes out and collects links. These links are then placed betewen some <a> tags and the result is saved to a .html file. This function is connected to an Azure storage blob where the html file is hosted and gets updated once a day at 4pm.

In order for the scanner to scan the site, it would need to be hosted on a domain matching the root domain of the sitemap <loc> tags (as the scanner only follows root domain links).

If you happen to be using Azure, we can walk through the finer details of some of the configuration that have been marked in gitignore. If you're using AWS, then it would be dependant on equivalents (how functions work, are integrated into a storage blob etc) for AWS specific functionalities. I'm happy to help with figuring this out if needed!
