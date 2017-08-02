
The player {{ hunt.hunter.email }} claims to have ghostified you in the game '{{ game.name }}'.


You can validate it directly at:
<{{ forms.players.GhostifiedPlayer.make_url(game, hunt.target) }}>

You can validate ghostification on your page too:
<{{ pages.players.Home.make_url(hunt.target) }}>

