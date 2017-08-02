Assassin's game started
=======================

The game '{{ game.name }}' is now running.

Your informations, status, score and target are available at:
<{{ pages.players.Home.make_url(player) }}>

You can validate ghostification on this page too.

Current target
--------------

Your current target is {{ player.current_target_for_game(game).email }}.

You will not know the player who targets you, until you're ghostified.

In each case, each players have to validate the ghostification.


Direct actions:

* if you ghostified the other player: <{{ forms.players.GhostifyPlayer.make_url(game, player) }}>
* if you have been ghostified by an other player: <{{ forms.players.GhostifiedPlayer.make_url(game, player) }}>



Good luck, have fun!

