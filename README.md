# :hammer_and_wrench: Stori QA Automation Engineer Challenge

## :pick: Daniel Felipe Hernández Mancipe

<br/>

This project is the solution for the `Stori QA Automation Engineer Challenge`.

## Getting Started

### Prerequisites

- Node.js => 20.14.0
- npm => 10.7.0
- Android Studio => Koala 2024.1.1
- Android SDK Platform => Android 13.0 ("Tiramisu") API Level 33
- Set up `ANDROID_HOME`
- Android SDK Platform-Tools => 35.0.1
- Android Emulator => 34.2.15
- Java JDK => 8
- Set up `JAVA_HOME`

### Installing

Install Appium using npm:

```bash
npm install -g appium
```

Install the UiAutomator2 driver:

```bash
appium driver install uiautomator2
```

Lastly, just clone this repository:

```bash
git clone <url>
```

### Using

Just call the runner with your desired browser and device:

```bash
python3 runner.py --browser <browser> --avd <avd>
```

The argument `browser` could be: `chrome` (by default), `firefox`, or `opera`.

The argument `avd` is the name of the Android Virtual Device that is set up, for instance, this is my test device via the Android Virtual Devices Manger of Android Studio:

![](../media/avd_from_avdm1.png?raw=true)

![](../media/avd_from_avdm2.png?raw=true)

What it looks like when running on Firefox:

![](../media/demo_firefox.gif?raw=true)

After the execution, the `XML` and `HTML` reports are generated in [`/reports/<browser>/pytest-html/report.html`](/reports/chrome/pytest-html/report.html) and [`/reports/<browser>/junit-xml/report.xml`](/reports/firefox/junit-xml/report.xml)

### RTM report

| Test Case ID      |                                                               Switch-Window-Header–Spelling                                                                |
| ----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Developer         |                                                                        Developer 1                                                                         |
| Test Group        |                                                                       UI – Spelling                                                                        |
| Test Case Name    |                                                                   Misspelling in header                                                                    |
| Priority/Severity |                                                                          low/low                                                                           |
| Test Steps        | 1. Go to `/AutomationPractice`<br>2. Go to `Switch Window Example` section<br>3. Click on `Open Window` button<br>4. See the `Opening Hours` in the header |
| Expected Result   |                                                                     Monday to Saturday                                                                     |
| Tester            |                                                                     Quality Engineer 1                                                                     |
| Actual Result     |                                                                     Monday to Saturay                                                                      |
| Status            |                                                                            Fail                                                                            |
| Evidence          |                                                            ![](../media/evidence1.png?raw=true)                                                            |

## Built With

- [Appium](https://appium.io/docs/en/2.9/) => 4.0.0 - UI automation (cross-browser and cross-platform)
- [Pytest](https://docs.pytest.org/en/8.2.x/) => 8.2.2 - Python testing framework
- [Pytest-BDD](https://pytest-bdd.readthedocs.io/en/stable/) => 7.2.0 - Subset of Gherkin for Python
- [Pytest-HTML](https://pypi.org/project/pytest-html/) => 4.1.1 - Plugin for generating HTML reports
- [Git](https://git-scm.com/) => 2.30.2 - Version Management

## Authors

- **Daniel Hernández** - _Initial work_ - [danielhndz](https://github.com/danielhndz)
- Last update: 24/07/2024

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
