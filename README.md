# local-show-tracker
[Theory] A python-made GUI that helps you locally keep track of your watch progress on TV shows that are terribly mapped by TraktTV, or other tracking services.

**THIS SCRIPT IS THE PRODUCT OF MULTIPLE LLM'S**
While it is not malicious (you can view the code yourself before you choose to run it), it is buggy, and I take no responsibility for that. This is a baseline, at best. At worst, a pleasant disaster :)

This will create a file called "show_data.json" with the following format:
{
    "**Show Title Here**": {
        "description": "**Description here**",
        "season": 1,
        "episode": 1,
        "cover_image": "**Path to cover image here**"
    }
}

*If you happen to stumble into this and want to make changes, create an issue. If I add the change, I will credit your GitHub profile in the updated code.*

## Requirements
- **A Linux system.** All of my testing is on an Arch-based system. I have no intention of testing this, or fixing it for, other operating systems. If it crashes and burns on Windows, then that is your homework to get it up and running.
- kdialog - for the file picker so you can add cover images for your shows. You are free to change this to whatever file picker you have on your system, or just not use cover images at all

In theory, everything else should be available on most common Linux distros, if not, you will get an error that tells you what exactly you are missing.

## Usage
`cd [path to show_tracker.py]`

If you cloned this repo to your home directory, the command would be:
`cd local-show-tracker`

Then, run the script:
`python3 show_tracker.py`
