import nextcord # type: ignore
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
            nextcord.SelectOption(
                label="Events", description="Be as bubbly as your drink! Events w/The Boys", emoji="<a:ohwait:1070504388797403186>", value="EVNT"
            ),
            nextcord.SelectOption(
                label="Flight Captain", description="Ready for takeoff. (Flight Simulator 2020)",emoji="🛫", value="FLY"
            ),
            nextcord.SelectOption(
                label="Naughty Nasty", description="NSFW Channels",emoji="🔞", value="NSFW"
            ),
            nextcord.SelectOption(
                label="Shitters", description="Shit on them, shit on ALL OF THEM!!!",emoji="💩", value="SHT"
            ),
            nextcord.SelectOption(
                label="Games", description="We count, we roll, we flipp",emoji="🎮", value="GAME"
            ),
            nextcord.SelectOption(
                label="Venting", description="We know you're in the vents, tell us what bothers you.",emoji="<:amongus:1011282397024755732>", value="VENT"
            ),
            nextcord.SelectOption(
                label="Streamer", description="P-P-P-POGGERRRRRSSSSS",emoji="💩", value="STRM"
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
            g.get_role(EVNT_ROLE),
            g.get_role(FLY_ROLE),
            g.get_role(SHT_ROLE),
            g.get_role(NSFW_ROLE),
            g.get_role(GAME_ROLE),
            g.get_role(VENT_ROLE),
            g.get_role(STRM_ROLE),
        ]
        
        # Check if user has the required role
        required_role = g.get_role(1210277151455314031)
        if required_role not in interaction.user.roles:
            await interaction.response.send_message("You do not have the required role to access this menu. Please contact staff for assistance.", ephemeral=True)
            return

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
            if choice == "EVNT":
                selected.append(roles[7])
            if choice == "FLY":
                selected.append(roles[8])
            if choice == "SHT":
                selected.append(roles[9])
            if choice == "NSFW":
                selected.append(roles[10])
            if choice == "GAME":
                selected.append(roles[11])
            if choice == "VENT":
                selected.append(roles[12])
            if choice == "STRM":
                selected.append(roles[13])

        
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