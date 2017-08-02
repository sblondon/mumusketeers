
The player {{ hunt.hunter.email }} claims you have ghostified him/her in the game '{{ game.name }}'.


You can validate it directly at:
<{{ forms.players.GhostifyPlayer.make_url(game, hunt.hunter) }}>

You can validate ghostification on your page too:
<{{ pages.players.Home.make_url(hunt.hunter) }}>

