<!--suppress ALL -->
<div align="center">
  <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
  <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/network/members" target="_blank">
    <img src="https://img.shields.io/github/forks/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge" alt="Forks">
  </a>
  <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
  <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge" alt="Forks">
  </a>
  <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/blob/master/LICENSE.txt" target="_blank">
    <img src="https://img.shields.io/github/license/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
</div>


<!-- PROJECT TITLE -->
<!--suppress HtmlDeprecatedAttribute, HtmlUnknownAnchorTarget -->

<div align="center">
<h3 align="center">ZBSchools - Macro</h3>
  <p align="center">
    Auto grinder for ZBSchools built with Python Selenium
    <br/>
    <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/issues">Report Bug</a>
    ·
    <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This is a rather simple Python script which makes use of Selenium's ability
to interact with the web browser to create a sophisticated bot capable of solving
most questions with absolute precision.

Some awesome features:
* Lightweight
* Runs in the background
* Solves nearly all questions
* Multi threaded
* Gain 12 million points per day (On 6 Threads)
* Instant setup and configurable

### Disclaimer
Use this program at your own risk. According to <a href="https://www.sph.com.sg/legal/website_tnc/">SPH Terms and Conditions</a>
Section 6 Part D, users must not "use any automated process, use any kind of scripting software or bots or service to access and/or use the Site and/or Services".
This program is merely demonstrating the capabilities of the Selenium webdriver, and you are liable
for all consequences of your actions.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation

Prerequisites: Cookie Editor browser extension, Chrome version 110 (Latest as of 19 Feb 2023)

1. Head to <a href="https://github.com/TheTrustyPwo/ZBSchools-Macro/releases/">Release</a> and download the release zip file
2. Once complete, extract the zip file
3. In the extracted folder, you should see 3 files, namely `main.exe`, `config.json` and `cookies.json`
4. Go to <a href="https://www.zbschools.sg/">ZBSchools</a> and sign in
5. Using the <a href="https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en">Cookie Editor</a> extension, export your cookies which should copy them to your clipboard
6. Open `cookies.json` and clear all the text in the file and paste your cookies in
7. Note that you need to do this every time your cookies change (Which depends on your activity)
8. Modify `config.json` to your liking. Refer to the section below.
9. Finally, run main.exe which will open a terminal

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONFIGURATION -->
## Configuration

This is a list of configurable options in the `config.json` file and what they mean.

| Configurable             | Description                                                                                                                                             | Default | Datatype |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------|
| `lastProcessedArticleID` | Saves the last processed article ID to prevent repeated processing. Do not modify this unless you know what you are doing.                              | 14      | int      |
| `articlesPerSession`     | Number of articles the script will process every time you run it. Once it processes that many articles, it will stop and exit.                          | 100     | int      |
| `threads`                | Number of threads to run. More threads means that the script will be able to solve more articles concurrently, but will also use more system resources. | 4       | int      | 
| `headless`               | If set to true, the browser will be invisible which increases performance. It is recommended to turn this on for quicker solving.                       | false   | bool     |

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

TheTrustyPwo - Pwo#0001 - thetrustypwo@gmail.com

Project Link: [https://github.com/TheTrustyPwo/ZBSchools-Macro](https://github.com/TheTrustyPwo/ZBSchools-Macro)

<p align="right">(<a href="#top">back to top</a>)</p>
