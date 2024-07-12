# cogs/blackjack.py
import discord
from discord.ext import commands
import random

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.high_scores = {}

    @commands.command(name='blackjack')
    async def blackjack(self, ctx):
        """Start a game of blackjack."""
        player_hand, dealer_hand = self.deal_initial_hands()
        self.games[ctx.author.id] = {
            'player_hand': player_hand,
            'dealer_hand': dealer_hand,
            'message': None,
            'ctx': ctx  # Store the context
        }
        await self.show_hands(ctx)

    def deal_initial_hands(self):
        """Deal initial hands for player and dealer."""
        deck = self.create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        return player_hand, dealer_hand

    def create_deck(self):
        """Create a standard deck of cards."""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(value, suit) for value in values for suit in suits]
        random.shuffle(deck)
        return deck

    async def show_hands(self, ctx):
        """Show the current hands to the player."""
        game = self.games[ctx.author.id]
        player_hand = game['player_hand']
        dealer_hand = game['dealer_hand']
        player_value = self.calculate_hand_value(player_hand)
        dealer_visible_value = self.calculate_hand_value([dealer_hand[0]])

        player_hand_str = ' '.join([f'{value} of {suit}' for value, suit in player_hand])
        dealer_hand_str = f'{dealer_hand[0][0]} of {dealer_hand[0][1]} and a hidden card'

        description = (f'Your hand: {player_hand_str} (Total: {player_value})\n'
                       f"Dealer's hand: {dealer_hand_str} (Visible Total: {dealer_visible_value})\n\n"
                       'React with 🇭 to hit or 🇸 to stay.')

        if game['message']:
            await game['message'].edit(content=description)
        else:
            game['message'] = await ctx.send(description)
            await game['message'].add_reaction('🇭')
            await game['message'].add_reaction('🇸')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reactions for hit or stay."""
        if user.bot:
            return

        if user.id in self.games and self.games[user.id]['message'].id == reaction.message.id:
            if reaction.emoji == '🇭':
                await self.hit(reaction.message.channel, user)
            elif reaction.emoji == '🇸':
                await self.stay(reaction.message.channel, user)

    async def hit(self, channel, user):
        """Handle hit action."""
        game = self.games[user.id]
        deck = self.create_deck()
        player_hand = game['player_hand']
        player_hand.append(deck.pop())

        if self.calculate_hand_value(player_hand) > 21:
            await self.end_game(user, won=False)
        else:
            # Use the original context (ctx) to call show_hands
            await self.show_hands(game['ctx'])

    async def stay(self, channel, user):
        """Handle stay action."""
        game = self.games[user.id]
        player_hand = game['player_hand']
        dealer_hand = game['dealer_hand']

        while self.calculate_hand_value(dealer_hand) < 17:
            deck = self.create_deck()
            dealer_hand.append(deck.pop())

        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        if player_value > dealer_value or dealer_value > 21:
            await self.end_game(user, won=True)
        else:
            await self.end_game(user, won=False)

    def calculate_hand_value(self, hand):
        """Calculate the value of a hand in blackjack."""
        value = 0
        aces = 0
        for card in hand:
            if card[0] in 'JQK':
                value += 10
            elif card[0] == 'A':
                value += 11
                aces += 1
            else:
                value += int(card[0])

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    async def end_game(self, user, won):
        """End the game and update high scores."""
        game = self.games.pop(user.id)
        player_hand = game['player_hand']
        dealer_hand = game['dealer_hand']
        player_hand_str = ' '.join([f'{value} of {suit}' for value, suit in player_hand])
        dealer_hand_str = ' '.join([f'{value} of {suit}' for value, suit in dealer_hand])
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        if won:
            self.high_scores[user.id] = self.high_scores.get(user.id, 0) + 1
            result = f'You win! Your hand: {player_hand_str} (Total: {player_value}), Dealer\'s hand: {dealer_hand_str} (Total: {dealer_value})'
        else:
            result = f'You lose! Your hand: {player_hand_str} (Total: {player_value}), Dealer\'s hand: {dealer_hand_str} (Total: {dealer_value})'

        await game['message'].edit(content=result)

    @commands.command(name='highscores')
    async def highscores(self, ctx):
        """Show the high score list."""
        high_score_list = sorted(self.high_scores.items(), key=lambda x: x[1], reverse=True)
        high_score_str = '\n'.join([f'{self.bot.get_user(user_id)}: {score}' for user_id, score in high_score_list])
        await ctx.send(f'High Scores:\n{high_score_str}')

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
