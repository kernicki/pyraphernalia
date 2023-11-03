#!/bin/bash
# setup variables
# cd /to/where/houdini installed and source ./houdini_setup

if [[ ! -z "$HFS" ]]; then
    HOUDINI_HOME="houdini$HOUDINI_MAJOR_RELEASE.$HOUDINI_MINOR_RELEASE"
    pane_conf="PaneTabTypeMenu.xml"
    user_pane_conf="$HOME/$HOUDINI_HOME/$pane_conf"
    if [ ! -f "$user_pane_conf" ];then
        cp "$HFS/houdini/PaneTabTypeMenu.xml" "$user_pane_conf"
    fi
    mkdir -pv "$HOME/$HOUDINI_HOME/python_panels"
    mkdir -pv "$HOME/$HOUDINI_HOME/python3.7libs"
    cp -vb vex_occur.py "$HOME/$HOUDINI_HOME/python3.7libs"
    cp -vb vex_occur.pypanel "$HOME/$HOUDINI_HOME/python_panels"
    if [ -f "$user_pane_conf" ];then
        if grep -Fq "vex_occur" "$user_pane_conf"
        then echo "vex_occur is already added to $user_pane_conf"
        else
            echo "adding a new entry to $user_pane_conf"
            s="s|</menu>|\t<actionItem id=\"pythonpanel::vex_occur\">\n\t\t<label>VEX Occur</label>\n\t</actionItem>\n</menu>|g"
            sed -i "$s" "$user_pane_conf"
        fi
    else
        echo "$user_pane_conf does not exist. Please copy manually."
    fi
else
    echo "Setup Houdini environment first by running ./houdini_setup in Houdini root directory."
fi
