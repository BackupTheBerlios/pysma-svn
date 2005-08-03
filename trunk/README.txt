===============================
o    |\      /  |\/|   /\     o
o o  |/  \/  \  |  |  |__|  o o
o    |   /   /  |  |  |  |    o
===============================

== Version ==
  0.3


== Copyrights ==
  See AUTHORS.txt file.


== License ==
  All files of this project are licensed relating to the terms of the GNU
General Public License. See COPYING.txt file for more details.


== Website ==
  https://developer.berlios.de/projects/pysma/


== Release notes for 0.3 ==
 - Last release notes are up to date for this release : see further.
 - The project is documented in the Epydoc format. To compile the document,
get Epydoc version 2.1 or later and compile it with the command at the
root of the project :
   epydoc -o doc -n "PySMA API" --private-css blue pysma
 - You can also download the "-doc" archive from the Berlios project site
and untar it in you PySMA root directory or in your /usr/share/doc directory
(or the equivalent on your system). It contains the HTML and the PDF version
of the API documentation.


== Notes for version 0.2 ==
  - This is the second release of pysma, the Python multi-agent platform.
  - This release is nearly completely different from 0.1 release ! There are no 
compatibility between these releases.
  - This release now manage Agent/Group/Role (AGR) model.
  - MassageManager is removed (kernel manage now message providing and agents ma
nage their message box).
  - Agent can have a name and a parent (Agent who launch it) -- Fields exist but
 no method to access their --
  - A new 'scheduler' module is appeared. Kernel don't schedule agents anymore, 
it just launch and kill their. Scheduler is an abstract class and works with Act
ivator which activates agent by a specific Group/Role couple.
  - As an example, a DummyScheduler class is implemented to show how can work a 
scheduler. It activates the Group/Role None/None, which is the default role wher
e all agents are (excepted DummyScheduler itself of course).
  - The package test 'hunt' has been updated to be compatible with the new relea
se. So it now uses roles instead of agent ids which can't be arbitrarly affected
 anymore.
  - To launch the example game, it's like the previous release ; go to the root 
of the project and type the command:
    PYTHONPATH=. python hunt/game.py [ARGS]

    Optionnal args can be :
    * width=<width of the toric world>
    * height=<height of the toric world>
    * predators=<number of predators in the simulation>

    Examples :
    PYTHONPATH=. python hunt/game.py
    PYTHONPATH=. python hunt/game.py width=5 height=5 predators=4
    PYTHONPATH=. python hunt/game.py predators=8
    PYTHONPATH=. python hunt/game.py width=10

    Enjoy!
    [NB: The prey agent is identified by [ ** ] in the display, other ids are pr
edators]
  - The objective of the prey/predator game is the capture of the prey by the pr
edators. The artificial intelligence is not very high. Agents move randomly ! Th
is game has just been coded to show you an example of use of PySMA. Don't hesita
te to study and modify the source code in order to understand its features.


