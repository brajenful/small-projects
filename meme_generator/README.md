# meme_generator

One of the many custom-made extensions for my private Discord bot. What it does it takes a standard meme template with x amount of panels, and puts parts of the passed string in their respective panels.

### Dependencies: 
Because this is an extensions for a discord bot, you'll have to have one already set up, and it needs to be using the rewrite branch of discord.py.
Also, for image processing, I used [Pillow](https://github.com/python-pillow/Pillow), so you'll need that as well.

### How to use:
I wanted to make this extension as modular and versatile as possible, and even though I didn't do a very good job, you should have seen what the code looked like when everything was hard-coded.

Anyway, the idea is that you have a config file (templates.json), which contains all the necessary information for the code to be able to do its thing (template paths, number of panels etc.). If you want to add a new template, all you need to do is add a new entry to the json file, put in all the necessary information for that template, create a new command, and tell it to use the new template.

You'll find more detailed instructions in the comments.

Keep in mind, this is by no mean a professional work, nor did I ever intend it to be. Yes, I know the code looks bad, and there's probably better ways to do what I did. Regardless, feedback and constructive criticism is welcome and appreciated.
