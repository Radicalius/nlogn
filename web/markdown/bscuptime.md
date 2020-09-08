> September 7, 2020
# BSC Uptime: Heartbeat Monitoring Webservice
[github](repo://bsc-uptime) [demo](demo://bscuptime)
---
For Demo:
* username: **admin@bscuptime.com**
* password: **admin**
* Please refrain from deleting/editing the example monitors (`always_up`, `always_down`)
---

In college I was in charge of IT for my cooperative.  We shared internet with another cooperative across the street.  As a result, our setup was quite different from that of a normal house.  Notably, we did not have any internet-facing static IP addresses.  This made it difficult to do monitoring and alerting of uptime, as most uptime services (e.g. [Uptime Robot](https://uptimerobot.com/) work by pinging a global IP address to see if it responds.  

[]()

Some uptime services also offer heartbeat monitoring.  In this scheme, the server being monitored sends periodic requests to the uptime service, which triggers an alert if it doesn't hear from the monitored server for a certain period of time.  This is analogous to a [dead man's switch](https://en.wikipedia.org/wiki/Dead_man%27s_switch), which is activated when a button is released.  In our case, we want to trigger an alert when the monitored server fails to check in, because this means it cannot reach the service's servers.   

[]()

I could use heartbeat monitoring to alert me when the internet at my coop goes down by setting up a heartbeat server in the house that talks to a service in the cloud.  If the heartbeat server failed to communicate with the service, then the coop is probably disconnected from the internet.  However, I was unable to easily find a free heartbeat monitoring service, so I decided to try to implement my own.

## Specification

The project would consist of two programs.  
1. A server hosted outside of the house that would listen for pings, keep track of whether the coop network was connected to the internet and send email alerts when the network's status changed


2. A client script that would run on a local server and periodically send requests to the server

Python is the first language taught at my school, so I decided that it would be practical to write the whole project in it, so that it might be more maintainable by my housemates.  I chose Flask + gunicorn stack for the remote server.  Postgres was a natural choice for a database, as it is free on heroku.  I chose to use the requests module for the client side script

[]()

Though not strictly necessary to the original goal, I decided to expand the project to include support for the following:
* Multiple monitors.  Perhaps it might be nice to have multiple servers in different parts of the house to check that the whole house has internet connectivity.
* Multiple users.  I figured that we weren't the only house in the Berkeley Student Cooperatives that might need this service.  So I figured it might be nice to add multiple accounts so different houses could administer their own monitors.
* Basic uptime statistics for the current day, week, and month.
* Spam protection.  The ping endpoint would be open to the public, meaning that anyone could mess with uptime numbers by sending pings to our server.
* A web frontend that would make the service more user-friendly.  Additionally the user interface would need to look nice, because people tend to throw out old-looking software.

## Implementation Details

### User Interface

The user interface is implemented in [jinja](https://palletsprojects.com/p/jinja/) templated html with embedded javascript.  To avoid reloading the page, actionable endpoints (i.e. `/add`, `/delete`, `/edit` monitors) are queried using `XmlHttpRequest`.  I used [Bootstrap](https://getbootstrap.com/) stylesheets to improve the site's appearance.  

### Accounts

To save some time, I decided to add accounts to the database manually as needed.  I didn't expect that there would need to be that many accounts, so creating a \'Create Account\' user interface seemed like a waste of time.  Upon visiting the site, users are prompted to sign in and are given a sessionid cookie that will authenticate them to perform further actions.  

> Note that I did not salt and hash the passwords in the database.  This was cumbersome when manually entering the passwords, so I decided to forego this security measure.  Given that the consequences of an attacker getting these passwords would be slight, I figured that this was justified.

### Monitors

Monitor state is tracked in the database.  Each monitor is associated with a user by a foreign key relation, and only that user has edit and delete access via the `/edit` and `/delete` endpoints.  The program also updates monitor state as requests are made to the `ping` endpoint.  A separate thread periodically queries the database to check that the last check in is less than 3 intervals old.  If it is older, then the thread updates the status of the monitor and sends a `DOWN` email alert.  If the monitors statues is down and the monitor was pinged recently, the thread sets the status to up and sends an `UP` email alert.  It also keeps track of the total number of downtime periods vs uptime periods for the current day, week, and month, so that this information can be displayed on the dashboard.   

### Spam Protection

Each monitor is assigned a randomly generated, 32 character, ascii string as a token.  When the client program is downloaded \(by logging in and clicking monitor name \=\> settings \=\> download client\) the string for the monitor is included in the program.  The client then `POST`s this token to the `/ping` endpoint over `https` to check in.  Getting the token would require an attacker to either hack into the database, hack into the user's account, intercept the message in transit and decrypt the token, or compromise the heartbeat server.  It seems highly unlikely that anyone would go through that much trouble just to troll me.

> Of course, this measure is not very useful if the rest of the site is not waterproof.  I took care to sanitize user input by using prepared queries and html escaping any data that might show up on the page (e.g monitor names).  This should help defend against common SQL-Injection and XSS related attacks.  I wouldn't be surprised if there are still some vulnerabilities in the site, but I think I've taken care of the low hanging fruit.  Advanced hackers are definitely outside the scope of my threat model.

## Conclusions

This service was used for a few semesters at my house.  During that time it functioned as intended; it alerted me to the few internet outages that occurred while I was managing the coops network.  However, there was very little interest in this service in other coops, and many of the issues that caused internet outages in my coop have been fixed.  Thus, I am retiring this project for now.
