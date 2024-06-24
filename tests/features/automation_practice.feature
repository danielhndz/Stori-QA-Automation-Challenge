Feature: Automation practice

  A site to practice automation.

  Background:
    Given the user is on the automation practice page

  @suggession_class
  Scenario Outline: Suggession class example
    When the user types <entry> and selects <country>
    Then the user can see <country> in the <element>
    Examples:
      |entry|country|element|
      |Me|Mexico|suggession_box|
      |Uni|United States (USA)|suggession_box|
      |Uni|United Arab Emirates|suggession_box|
      |Col|Colombia|suggession_box|

  @dropdown
  Scenario Outline: Dropdown example
    When the user scrolls at the <direction> to the <element>
    And the user selects the option <option> from the <element>
    Then the user can see <option> in the <element>
    Examples:
      |direction|element|option|
      |right|dropdown|Option2|
      |right|dropdown|Option3|
  
  @switch_window
  Scenario: Switch window example
    When the user clicks on the "Open Window" button
    Then the user can see a message titled "30 DAY MONEY BACK GUARANTEE" with the following body:
      We would never want you to be unhappy! If you are 
      unsatisfied with your purchase, contact us in the first 30 days 
      and we will give you a full refund.
  
  @switch_tab
  Scenario: Switch tab example
    When the user clicks on the "Open Tab" button
    And the user clicks on the hamburger icon
    Then the user takes a screenshot
    And the user switches to the previous tab
  
  @switch_alert
  Scenario Outline: Switch alert example
    When the user types <entry> in the <element>
    And the user clicks on the <button> button
    Then the user can see an alert with this message <msg>
    And the user clicks on the "OK" button
    Examples:
      |entry|element|button|msg|
      |Stori Card|alert_box|Alert|Hello Stori Card, share this practice page and share your knowledge|
      |Stori Card|alert_box|Confirm|Hello Stori Card, Are you sure you want to confirm?|

  @web_table
  Scenario Outline: Web table example
    When the user sees how many courses cost $<price>
    Then the user can see its names
    Examples:
      |price|
      |25|
      |15|

  @web_table_fixed_header
  Scenario Outline: Web table fixed header example
    Then the user can see the names of the people with the <position> position
    Examples:
      |position|
      |Engineer|
      |Businessman|

  @iframe
  Scenario: iFrame example
    Then the user can see in the iFrame this text:
      His mentorship program is most after in 
      the software testing community with long 
      waiting period. 