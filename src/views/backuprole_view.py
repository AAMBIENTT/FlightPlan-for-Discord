import nextcord # type: ignore
from nextcord.ext import commands # type: ignore

from config import *


# Dropdown object
class Dropdown(nextcord.ui.Select):
    # Constructor
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label="VRChat Degen", description="Ready for ERP?", emoji="<:tvf_verrchud:1038277528227422328>", value="VRC"
            ),
            nextcord.SelectOption(
                label="Time Check", description="4:20 Pings ", emoji="<a:weed:1161444086255988747>", value="TMC"
            ),
            nextcord.SelectOption(
                label="Beat Saber", description="Wanna have a sword fight?", emoji="<:bsbuddy:1221902477369282781>", value="BS"
            ),
            nextcord.SelectOption(
                label="Rizz", description="Are you the Rizzler? Roll to find out.", emoji="<:sunglasses3dverycool:708503312504193082>", value="RIZ"
            ),
            nextcord.SelectOption(
                label="Color of the Day", description="I'm RGB as fucc boiiii!", emoji="<:Jfuzyowo:1217012345977573476>", value="COTD"
            ),
            nextcord.SelectOption(
                label="Bot Updates", description="I'll harass you when i get updated", emoji="<:Jfuzyowo:1217012345977573476>", value="BU"
            ),
            nextcord.SelectOption(
                label="Game Dealz", description="Lamp oil? Rope? Bombs? You want it? It's yours my friend! As long as you have enough Dollars!", emoji="<:fallenbab:1222628649790996490>", value="GDZ"
            ),
        ]

        # Dropdown settings
        super().__init__(
            placeholder="Choose your role...",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id="dropdown_role_selection"
        )

    # Dropdown reaction
    async def callback(self, interaction: nextcord.Interaction):
        g = interaction.guild
        roles = [
            g.get_role(VRC_ROLE), 
            g.get_role(TMC_ROLE), 
            g.get_role(BS_ROLE), 
            g.get_role(RIZ_ROLE),
            g.get_role(COTD_ROLE),
            g.get_role(BU_ROLE),
            g.get_role(GDZ_ROLE),
        ]
        
        # Loop through Dropdown selections
        selected = []
        for choice in self.values:
            if choice == "VRC":
                selected.append(roles[0])
            if choice == "TMC":
                selected.append(roles[1])
            if choice == "BS":
                selected.append(roles[2])
            if choice == "RIZ":
                selected.append(roles[3])
            if choice == "COTD":
                selected.append(roles[4])
            if choice == "BU":
                selected.append(roles[5])
            if choice == "GDZ":
                selected.append(roles[6])

        
        roles_add = []
        roles_remove = []
        response_msg = ""
        # Loop through each role
        for role in roles:
            
            # Check if role is wanted
            if role in selected:
                if role not in interaction.user.roles:
                    response_msg += f"You like **{role.name}**!\n"
                    roles_add.append(role)
            else:
                if role in interaction.user.roles:
                    response_msg += f"You dislike **{role.name}**!\n"
                    roles_remove.append(role)
        
        # Make member changes
        member = interaction.user
        await member.add_roles(*roles_add)
        await member.remove_roles(*roles_remove)
        if response_msg == "": # Incase nothing changed
            response_msg += f"You didn't make any alterations ***NERD!***"
        await interaction.response.send_message(response_msg, ephemeral=True)


# View object
class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())