# RogueAP (EvilTwins)

## How it works

The "Evil Twin" attack come from the category of "phishing" attack. It main goal is to copy an access point with the same name to finally connect the victim to this access point and take the informations he enter while connected.

That's how Evil Twin work:

The hacker will disturb the connection to the user. This user will reconnect to the Evil Twin the hacker created which will allow him to know every informations he will put during his connection.

## Our Evil Twin automation script

With my colleagues, we created a script who can automate the attack in Python:

Firstly, for the fun, we print our banner;

We will now check for root privileges;

Then we get a list of equipments from /sys/classe/net;

After this, we processing the interfaces into a readable dictionnary, and we print it;

Now, we ask to the user which interface do he want to use;

We check if the choice is good, if it is, we print him what he chose;

We scan for APs with the interface and parse the list with AWK;

After this, we processing the APs into a readable dictionnary, and we print it;

The user will now choose his prefered target;

We will now processing the target choice into a readable dictionnary;

We can "launch" an Evil Twin, setting interface IP address;

We allow forwarding and put interface in ip tables;

We copy the dnsmasq and hostapd templates in the working directory;

We modify the templates;

Then we use the config files generated to start both hostapd and dnsmasq;

And in order to record what went through the evil twin we use tcpdump;