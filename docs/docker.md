-----

*Work in Progress*

# Using Docker to Run Transcribe

The beauty of using **`docker`** to run our **`transcribe`** script is that it handles
all the dependencies for you.

All you need is to have **`docker`** installed on your system and the **`Dockerfile`** found at
the top-level of this repository.

You can then do the following to transcribe your video files to SRT subtitle text files:

```bash
$ cd ~/projects/transcribe # Change directory to the directory which contains the Dockerfile.
$ docker run -v ~/projects/Bonsai_Tutorials:/tutorials
```

*Work in Progress*

-----
