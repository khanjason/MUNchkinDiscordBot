# MUNchkin

A discord bot for Model United Nations.

## Installation

MUNchkin is running on Heroku. To add the bot to your own server, click [here](https://bit.ly/2TQ8hcp).
Make sure MUNchkin has the correct roles needed to access any channels that it will use.
The 'Chair' role is required to use Chair commands. Delegate commands can used by anyone.

## Commands

MUNchkin has a variety of commands used to aid online MUN sessions in discord. To start a session, write:

```
!startSession
```
This enables the rest of the commands for use.

MUNchkin has a help facility which can be used by calling !help to list all commands. More help on a certain command can be retrieved by calling:
```
!help [command name]
```
Below is the list of help information for each command:
```
Chair Commands:

!startSession 
Enables all commands for a session and invites bot to voice channel.

!register [delegate name] [status]
Status can be present (p),present and voting(pv) or absent (a)

!viewRegister
Displays all registered delegations and their statuses.

!GS
Prints out the current general speakers list.

!popGS
Remove first delegate from general speakers list.
Used just after a speaker has finished.

!speak [delegate name] [time in seconds]
Yields the floor to the delegate. Starts a timer.

!propose mod [total time in min] [speakers time in sec] [country proposed] [topic]
Propose a moderated caucus.

!propose [unmod or other] [total time in min] [country proposed]
Propose an unmod or other type of caucus.

!mod [total time in min]
Starts a timer for Mod.

!unmod [total time in min]
Starts a timer for Unmod.

!voting [topic]
Starts a non-caucus vote. Useful for final vote or amendments.

!endSession
Disables session commands and disconnects bot from voice channel.
Clears GS list.

!chair [@member]
Gives chair role to another member.

Delegate Commands:

!addGS
Adds your name to the general speakers list.

!tap
Alerts that you support the current debate.

!preamble
Displays list of phrases, useful for preambulatory clauses.

!operative
Displays list of phrases, useful for operative clauses.

!about
Provides information about MUNchkin.

!rules
Provides simplified ruleset for Harvard style MUN.
```


## Contributing
Contributions are not open at this stage. Come back soon for updates, star and watch this repository.

## License
[GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)
