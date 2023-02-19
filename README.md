[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU GPLv3 License][license-shield]][license-url]


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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This is a rather simple Python script which makes use of Selenium's ability
to interact with the web browser to create a sophisticated bot capable of solving
most questions with absolute precision. With this implementation, an article would be
solved in roughly 3.5 seconds, and after some benchmarking, it was found that 4 million
points could be obtained within the timespan of 24 hours, if the script is continuously
running of course.

### Disclaimer
Use this program at your own risk. According to <a href="https://www.sph.com.sg/legal/website_tnc/">SPH Terms and Conditions</a>
Section 6 Part D, users must not "not to use any automated process, use any kind of scripting software or bots or service to access and/or use the Site and/or Services".
This program is merely demonstrating the capabilities of the Selenium webdriver, and you are liable
for all consequences of your actions.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation

Prerequisites: Cookie Editor browser extension, Chrome version 110 (Latest as of 19 Feb 2023)

1. Head to https://github.com/TheTrustyPwo/ZBSchools-Macro/releases/ and download the release zip file
2. Once complete, extract the zip file
3. In the extracted folder, you should see 3 files, namely `main.exe`, `config.json` and `cookies.json`
4. Go to https://www.zbschools.sg/ and sign in
5. Using the <a href="https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en">Cookie Editor</a> extension, export your cookies which should copy them to your clipboard
6. Open cookies.json and clear all the text in the file and paste your cookies in
7. Note that you need to do this every time your cookies change (Which depends on your activity)
8. You may choose to modify `articlesPerSession` in `config.json` which determines how many articles the script will solve every time you run the executable (If you want to run it overnight, just set it to a large number)
9. Do not touch `lastSolvedArticleID` unless you know what you are doing as this prevents repeatedly solving of articles
10. Finally, run main.exe which should open a terminal


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


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge
[contributors-url]: https://github.com/TheTrustyPwo/ZBSchools-Macro/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge
[forks-url]: https://github.com/TheTrustyPwo/ZBSchools-Macro/network/members
[stars-shield]: https://img.shields.io/github/stars/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge
[stars-url]: https://github.com/TheTrustyPwo/ZBSchools-Macro/stargazers
[issues-shield]: https://img.shields.io/github/issues/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge
[issues-url]: https://github.com/TheTrustyPwo/ZBSchools-Macro/issues
[license-shield]: https://img.shields.io/github/license/TheTrustyPwo/ZBSchools-Macro.svg?style=for-the-badge
[license-url]: https://github.com/TheTrustyPwo/ZBSchools-Macro/blob/master/LICENSE.txt