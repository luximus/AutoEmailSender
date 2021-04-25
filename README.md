# AutoEmailSender
Automatically send an e-mail to all of your contacts

*(This project follows a tutorial by the people at [Hack Club](https://workshops.hackclub.com/). Go check it out!)*

## Usage
1. Log in to your Gmail account.
2. Go to [this website](https://myaccount.google.com/u/0/lesssecureapps?hl=en) and disable secure app access.
   Make sure to enable it again after using this.
3. Modify the `contacts.txt` file with all of your contacts. The format should be `<email>; <name>`. 
   The following is an example:
   
        bobsmith@johndoe.com; Bob
        johnappleseed@icloud.com; Mr. Appleseed
        ilikebutts@hotmail.com; Dr. Horny
        luximus100@gmail.com; Luximus

4. Modify the `message.txt` file with the message. The first line should be the subject of the e-mail, and every
   subsequent line should contain the message. Use `{0}` wherever you want the recipient's name to be, and
   `{1}` wherever you want your name to be.
   The following is an example:
   
        Business Proposal
        
        Dear {0},

            Bacon ipsum dolor amet boudin est pig hamburger qui swine kevin ball tip. Salami strip steak pariatur filet mignon, porchetta velit meatball consectetur brisket ut excepteur boudin. Shankle in est beef sunt brisket ut tempor chicken burgdoggen cow. Pancetta ad tri-tip meatloaf. Ad chislic shank boudin pancetta.

            Et meatloaf incididunt swine sunt. Ball tip alcatra occaecat quis, kevin frankfurter eiusmod. Dolore capicola velit venison tail jerky rump ham hock short loin enim shoulder chuck spare ribs. Cupim tail esse rump drumstick sirloin incididunt ipsum pork loin voluptate. Aute irure hamburger in ex pariatur shankle tri-tip landjaeger id cupim. Beef ribs officia flank, est laboris duis doner ball tip minim frankfurter tri-tip do reprehenderit.
        
        Sincerely,
        Sir Porkster
   
   *(If you're wondering where I got that filler text,
   go to [Bacon Ipsum](https://baconipsum.com/?paras=5&type=all-meat&start-with-lorem=1))*

5. Make sure your working directory is set to AutoEmailSender, and run `python main.py`.