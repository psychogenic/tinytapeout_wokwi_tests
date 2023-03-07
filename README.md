### Test framework for stable wokwi projects (e.g. hosted on tinytapeout site)

(C) 2023 Pat Deegan, https://psychogenic.com


This system allows for testing and inspection of wokwi projects on local system, and decouples the project from the tests in a way that allows them to be applied to wokwi projects without impacting them in any way.

In a fresh install, running

    WOKWI_PROJECT_ID=1234SOMEWOKWIID make runtest


 * will download the project template and tools required;
 * download the wokwi project with ID WOKWI_PROJECT_ID; 
 * configure the local project appropriately;
 * set it up with tests found in testmodules/WOKWI_PROJECT_ID; and
 * run those tests.

At this point, there are samples for a few wokwi projects, so running

    WOKWI_PROJECT_ID=346662951270220372 make runtest
    WOKWI_PROJECT_ID=347019916696617554 make runtest
    WOKWI_PROJECT_ID=347144898258928211 make runtest or
    WOKWI_PROJECT_ID=347497504164545108 make runtest

in a suitable environment (i.e. with cocotb etc installed) is all that is needed.

Other interesting make targets include

    WOKWI_PROJECT_ID=XYZ make show_module
    WOKWI_PROJECT_ID=XYZ make yosys_shell
    and
    WOKWI_PROJECT_ID=XYZ make show_truthtable # for combinatorial logic on io in/out


