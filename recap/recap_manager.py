"""Methods for formatting recaps from tab-based lists into WorldAnvil/BBcode"""


def format_recap(text):
    """take a string containing lines that are tab-indented.
    Output BBCode for WorldAnvil"""
    link_map = init_links()
    lines = text.splitlines()
    length = len(lines)
    formatted = []
    i = 0
    while i < length:
        # for i in range(length):
        this_line = lines[i]
        if i == 0:
            # assume first line is date
            formatted.extend(make_date_line(this_line))
            formatted.append("[ul]")
            i = i+1
            continue
        if i == (length-1):
            next_line = None
        else:
            next_line = lines[i+1]
        this_line_indent_level = get_indent_level(this_line)
        next_line_indent_level = get_indent_level(next_line)

        if this_line.isspace() or this_line == "":  # empty line - get ready for a date
            formatted.append("[/ul]")
            while lines[i].isspace() or lines[i] == "":
                i = i+1
            # line should be date
            formatted.extend(make_date_line(lines[i]))
            formatted.append("[ul]")
            i = i+1
            continue

        this_line = make_links(this_line, link_map)
        this_line = this_line.strip()
        this_line = indent(this_line_indent_level)+"[li]"+this_line
        if this_line_indent_level == next_line_indent_level:  # same list level
            this_line = this_line+"[/li]"
            formatted.append(this_line)
        elif this_line_indent_level < next_line_indent_level:  # start of deeper list
            formatted.append(this_line)
            formatted.append(indent(next_line_indent_level)+"[ul]")
        else:  # thisLineIndentLevel>nextLineIndentLevel - end of nested list
            this_line = this_line+"[/li]"
            formatted.append(this_line)
            current_nest_level = this_line_indent_level
            while current_nest_level > next_line_indent_level:
                formatted.append(indent(current_nest_level)+"[/ul]")
                formatted.append(indent(current_nest_level-1)+"[/li]")
                current_nest_level -= 1
        i = i+1
    formatted.append("[/ul]")
    line_sep = "\n"
    return line_sep.join(formatted)


def get_indent_level(line):
    "find the indent level of a line"
    if line is None:
        return 0
    if line.isspace():
        return 0
    return line.count('\t')


def make_date_line(line):
    "make the line into a date header.  Assumes already at zero-indent, returns a list"
    day_names = ["Gods' Day", "Forge Day", "Coin Day",
                 "Sprout Day", "Tomes Day", "Flames Day"]
    if not 'Day' in line:
        str_date = line.rstrip(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,')
        if str_date.isnumeric():
            date = int(str_date)
            day = day_names[date%6]
            line = line +", "+day


    formatted = [
        '[b]' + line + '[/b]',
        '[hr]'
    ]
    return formatted


def make_links(line, link_map):
    "replace instances of special names and places with worldanvil links"
    for key in link_map:
        if line.find(key) >= 0:
            line = line.replace(key, "@["+key+"]"+link_map[key], 1)
    return line


def indent(indent_level):
    "indent a line to the specified indent level"
    # what's the efficient way to do this?
    txt = ''
    for _ in range(indent_level):
        txt = txt+"\t"
    return txt


def add_link_entry(tag, *args):
    "used for populating the entries in the link map"
    this_map = {}
    name = tag[2:tag.index(']')]
    link_index = tag.index(']')+1
    link = tag[link_index:]
    this_map[name] = link
    for other_name in args:
        this_map[other_name] = link
    return this_map


def init_links():
    "initalize list of links for replacement"
    link_map = {}
    link_map.update(add_link_entry(
        "@[Graham](person:7fda6bf6-7a78-40e6-934f-43c4f06d1540)", "Graham Hayward"))
    link_map.update(add_link_entry(
        "@[Celduin](person:6da69324-d324-41a1-8931-d6b72e0c73c4)"))
    link_map.update(add_link_entry(
        "@[Ardr](person:7d7f9110-e15d-458d-af8e-d21f0ad3982b)"))
    link_map.update(add_link_entry(
        "@[Gilda](person:8a644e93-53f1-4d05-a661-407ca703b19c)", "Gilda Gonne"))
    link_map.update(add_link_entry(
        "@[Fedaria](person:eb7b59b3-81a8-42f5-b628-151da32436b8)", "Fedaria Quinn"))
    link_map.update(add_link_entry("@[Rosie](person:08dee44c-a760-4308-9011-35af77cf5dba)",
                                   "Rosie of the Glittering Coast"))
    link_map.update(add_link_entry(
        "@[Daermir](person:be55dabc-1761-4ff5-93f2-8d7239deb0ed)"))
    link_map.update(add_link_entry(
        "@[Lysivia](person:f9b4be98-bbd2-4cbf-a2e0-c13f1d0796a7)"))
    link_map.update(add_link_entry(
        "@[Tobias](person:c06484d7-b27e-41d2-9ba0-dabdaec502c3)", "Toby"))
    link_map.update(add_link_entry(
        "@[Dotmoul Smeltspine](person:5ce1a9ba-63da-41d9-a22e-ca4cd90981e4)"))
    link_map.update(add_link_entry("@[Breaker](person:62f309c5-a5fd-4489-a1d8-be40337da877)",
                                   "Breaker of the Seventh Star"))
    link_map.update(add_link_entry(
        "@[Esta](person:1523c000-9148-4d7e-add1-d2825aecdd5b)", "Esta Damsev"))
    link_map.update(add_link_entry(
        "@[Arthund](person:c0116e17-6382-44ab-b089-9696041902a6)"))
    link_map.update(add_link_entry(
        "@[Blue](person:a44d91c7-cf06-458a-a2ea-d00c9263b68a)"))
    link_map.update(add_link_entry(
        "@[Gareholm](settlement:c572cfb7-9024-401e-834c-73284278093b)"))
    link_map.update(add_link_entry(
        "@[Volantis](settlement:8688cefc-ba76-46ac-9dce-fc29e48b14e2)"))
    link_map.update(add_link_entry(
        "@[Gods' Watch](settlement:dcddce0a-0056-484b-9fc2-6cb171704a98)"))
    link_map.update(add_link_entry(
        "@[Highmount](location:40d004e4-5e73-4a90-984d-e60fadc0b8f6)"))
    link_map.update(add_link_entry(
        "@[Shard Armament](article:957e1458-ed13-48fe-bc14-0e17f9360f7a)"))
    link_map.update(add_link_entry(
        "@[Thousand Eyes](organization:999ac77a-34ea-4344-8b36-97cf930f6ef3)"))
    link_map.update(add_link_entry(
        "@[Adlem's Quay](settlement:454ed8ea-0866-479e-8b13-b911e6378d34)"))
    link_map.update(add_link_entry(
        "@[Eadwic Vyncis](person:c71659fd-022d-49dd-99b1-5bf9c6c6d445)"))
    link_map.update(add_link_entry(
        "@[Lindor's Rest](location:8718d1b5-d602-4101-9ad9-6c2f6521614b)"))
    link_map.update(add_link_entry(
        "@[Silvius](organization:7a39665c-d367-4df1-8866-eb3e6a44f7c5)"))
    link_map.update(add_link_entry(
        "@[Brunhild](organization:f02499fc-8ddb-443d-b5ac-dc34b1bbd119)"))
    link_map.update(add_link_entry(
        "@[Pyrrhus](organization:e5539076-3535-4110-8ba4-3d4d59537969)"))
    link_map.update(add_link_entry(
        "@[Acid Wastes](location:ebe447ec-88f3-4ebb-b196-78a5913c7a36)"))
    link_map.update(add_link_entry(
        "@[The Fly By Night](vehicle:25646caa-f0a8-4eba-9b49-ca15b7fd09e5)"))
    link_map.update(add_link_entry(
        "@[Gregory](person:4570f0d0-6a2e-402e-a8b6-9e48b91dbdc6)", "Big Greg"))
    link_map.update(add_link_entry(
        "@[Yrrasil](person:2f490b36-728e-4746-a002-950877d81295)"))
    link_map.update(add_link_entry(
        "@[Red Gulch](settlement:50d2162c-2178-4819-a102-668327846ff9)"))
    link_map.update(add_link_entry(
        "@[Brightseeker Bolviar](person:dcc56c5d-b347-4eee-bd10-a1e260ebba55)", "Bolviar"))
    link_map.update(add_link_entry(
        "@[Imera](person:5ed14923-fb04-4368-8a60-f13c6267d51b)"))
    link_map.update(add_link_entry(
        "@[Mosnadyn](person:68b497aa-a3d1-4853-88f2-65d9ed79dc10)"))
    link_map.update(add_link_entry(
        "@[Nax](person:b21c5e23-e59f-4c69-bc5c-ebb3c321710b)"))
    link_map.update(add_link_entry(
        "@[Nokozza](person:f4abb40c-0ff4-41f3-a3f6-cae1a515fc53)"))
    link_map.update(add_link_entry(
        "@[Ladore](person:beba0263-925f-404c-800d-fa0e150e77b7)"))
    link_map.update(add_link_entry(
        "@[Precursor](myth:2a20fe93-bad6-414e-a5b3-422ef9633ff0)"))
    link_map.update(add_link_entry(
        "@[Davaros](person:e300e345-f2b0-4cbb-9bbc-8ca7c0b1a4ac)"))
    link_map.update(add_link_entry(
        "@[Erlathan Dara](person:a86a4569-402f-406e-82b1-5a7c45d8271d)"))
    link_map.update(add_link_entry(
        "@[Elderwood](settlement:ef1bdca1-6c39-4c59-bd3d-c54cf9548474)"))
    link_map.update(add_link_entry(
        "@[Shayel Wynric](person:7e0247e6-93e8-480f-892c-5cba500307fa)"))
    link_map.update(add_link_entry(
        "@[Alexandre](person:3dda306e-c1fa-4d18-896c-1964da3c9257)", "Alexandre Sinter"))
    link_map.update(add_link_entry(
        "@[Artura](person:2a76e14c-6377-47e1-a179-51760e3e8293)", "Artura Verdugo"))
    link_map.update(add_link_entry(
        "@[Skarun](person:70066efe-db7e-4df9-95c7-a20e7a8cedd4)"))
    link_map.update(add_link_entry(
        "@[Celestia](organization:6fd69007-4b44-4872-93ae-5b5ac525ac52)"))
    link_map.update(add_link_entry(
        "@[Kadra](person:c8bf0825-76cb-4023-8825-fc4009a1a46f)"))
    link_map.update(add_link_entry(
        "@[Sanzir](person:efea694e-9956-4241-9e5f-12c8b88e793b)"))
    return link_map


def main():
    intext = """18th of Owl
On her way back to the ship, Fedaria is stopped by Irina, who asks how it is that a group of mercenaries got so close to the Pyrrhan royalty.  Fedaria only says that there’s a story behind it, but its not entirely hers to tell.
Alexandre briefly visits the Fly by Night, and speaks with Graham.  He asks Graham how someone from a Thell noble house came to be wearing Pyrrahn roughs clothing, to which Graham only says there were unfortunate events that disrupted seats of power within his house, and he left because he wasn’t prepared for it.  Alexandre expresses interest in the concerns of the Pyrrhan people, and Graham tells him they’re just normal people concerned about the king’s decisions, but they mostly worry how policy affects them rather than caring about who’s on the throne
Mars, Kiera, and Rosie train once again on the Firebrand, and after they are exhausted with practice,head back to the Fly by Night
Back on the ship, they get a whiff of an odd smell, start feeling light headed - Gilda passes out
	Graham recognizes the smell as an illicit drug, and the crew sees the source of the smell - a burning island in their path towards Elderwood
	Mars brings Gilda downstairs and Fedaria uses Lesser Restoration on her, and once the ship gets upwind of the wafting smoke, a Sylvan airship is spotted, with a shimmering aura and a massive flamethrower, atypical to the Sylvan ship style
	The Firebrand peels off to get more distance and continue towards Elderwood, and the Fly-by-Night follows the odd ship until they get feel for its path - heading towards an isthmus on the southwestern side of the continent
Catching back up to the Firebrand, the Midnight Crew escorts the Pyrrhans the rest of the way to their destination
On the way, Rosie works on her heat rune, and Graham completes his rework of his rifle into the Vindication

19th of Owl
In the morning, Kiera, Rosie, and Mars train once again with the Pyrrhans, and pick up a solid understanding of the one-handed, defensive sword technique
The Fly-by-Night and Firebrand dock separately, and the two groups plan to meet up after the Pyrrahns and the emissary establish their agenda
	The Midnight Crew checks into the Green Cap, where Davaros greets them, and Yon comes bounding out to hug Gilda/Ariel
	Gilda explains that she’s looking like Mags for the time being and going by “Ariel”
	She introduces Mars and Kiera, who are new to Yon
	Graham starts going by “Garrison”, and begins wearing a new outfit
Over lunch at the Green Cap, Toby attempts scrying on the twins
	He is able to see them at a bar, with several people with odd expressions around them, and a bartender with a black shirt, brown hair, and a broken nose nearby
	The twins were able to “look at” Toby’s scrying point, striking it and ending the spell
	Upon describing the scene to Davaros, he says the bar may be in the human enclave area of the city
	The crew discusses their options, and decide to strike while the opportunity is present and try to find the twins
Walking to the nearby human enclave, a district where illicit activities and some shady business are common, the crew finds and questions several people on a bar crawl, and learn that the broken-nosed man seen during the scrying was likely Johnny of the Hammered Bronze bar
	The crew makes use of Doctor Who to scope out the area, and find several entrances to the bar but no indication which floor the twins may be on
	After a strategic discussion about whether they should try to draw the twins outside or surprise them inside the bar, they decide to split up and tackle each of the three entrances in pairs to find and strike them down as quickly as possible
Each of the Midnight Crew members advances through the Hammered Bronze, sighting the twins and attacking instantly
	Rosie is overcome by a spell that causes her to not recognize anyone, but shakes it off to impart some devastating strikes on the twins
	Toby is knocked away from one of the treetop entrances, falling, but moving back up to the fight
	Gilda summons her spirit guardians, this time taking on the appearance of her fallen circus friends that the twins killed
	Mars clambers across the bar, raging and swinging wildly at the twins
	Kiera punches and kicks her way through the crowd, getting multiple hits in
	Graham gets a killing shot on one twin, but when her sister goes to strike him with magical lightning, Fedaria stealthily counterspells it
	Several dazed-looking bar patrons come to the defense of the twins, obviously compelled in some way.
Seeing that the odds are against her, the sister bearing the lute armament teleports out of sight
	Rosie dashes after her, the others following right after
	Spotting her just outside one upper entrance, the Midnight Crew lashes out to prevent her from getting away
	Gilda gets the final strike on the lute bearer, cutting her down with the summoned images of Mags and Amber, and the lute bearer falls to the ground below
	The team splits as some move towards the body and armament below, while some go to check on the bar patrons who got mixed up in the hectic combat and were hurt
"""

    outtext = format_recap(intext)
    print(outtext)


if __name__ == '__main__':
    main()