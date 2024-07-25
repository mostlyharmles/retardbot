# cogs/blackjack.py
import discord
from discord.ext import commands
import random
import os
from PIL import Image
import asyncio

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
#        self.high_scores = {}
        self.delete_delay = 90  # 5 minutes in seconds
        self.card_images_path = 'cards/'  # Path to card images
        self.temp_path = 'temp/'  # Path to temporary files

        # Ensure the temp directory exists
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

    @commands.command(name='blackjack', aliases=['bj', 'whitejack', 'wj', 'BJ','WJ'])
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
        # Schedule message deletion
        await ctx.message.delete(delay=self.delete_delay)

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

    def create_hand_image(self, hand, hidden=False):
        """Create an image representing the given hand."""
        card_width, card_height = 200, 300  # Adjust based on your card image sizes
        spacing = 10
        total_width = card_width * len(hand) + spacing * (len(hand) - 1)
        total_height = card_height

        hand_image = Image.new('RGBA', (total_width, total_height), (255, 255, 255, 0))
        for i, (value, suit) in enumerate(hand):
            card_path = os.path.join(self.card_images_path, f'{value}_of_{suit}.png')
            print(f'Trying to open card image: {card_path}')
            if hidden and i != 0:
                card_image = Image.open(os.path.join(self.card_images_path, 'back.png')).resize((card_width, card_height))
            else:
                try:
                    card_image = Image.open(card_path).resize((card_width, card_height))
                except FileNotFoundError:
                    print(f'File not found: {card_path}')
                    card_image = Image.new('RGBA', (card_width, card_height), (255, 0, 0, 0))  # Red placeholder for missing image
            hand_image.paste(card_image, (i * (card_width + spacing), 0), card_image)

        return hand_image

    async def show_hands(self, ctx):
        """Show the current hands to the player."""
        game = self.games[ctx.author.id]
        player_hand = game['player_hand']
        dealer_hand = game['dealer_hand']
        player_value = self.calculate_hand_value(player_hand)
        dealer_visible_value = self.calculate_hand_value([dealer_hand[0]])

        player_hand_image = self.create_hand_image(player_hand)
        dealer_hand_image = self.create_hand_image(dealer_hand, hidden=True)

        player_hand_image_path = os.path.join(self.temp_path, f'player_hand_{ctx.author.id}.png')
        dealer_hand_image_path = os.path.join(self.temp_path, f'dealer_hand_{ctx.author.id}.png')

        player_hand_image.save(player_hand_image_path)
        dealer_hand_image.save(dealer_hand_image_path)

        embed = discord.Embed(
            title="Blackjack",
            description=(f'Your hand: (Total: {player_value})\n'
                         f"Dealer's hand: (Visible Total: {dealer_visible_value})\n\n"
                         'React with 🇭 to hit or 🇸 to stay.')
        )
        embed.set_image(url=f'attachment://player_hand_{ctx.author.id}.png')

        if game['message']:
            files = [
                discord.File(player_hand_image_path, filename=f'player_hand_{ctx.author.id}.png'),
                discord.File(dealer_hand_image_path, filename=f'dealer_hand_{ctx.author.id}.png')
            ]
            await game['message'].edit(embed=embed, attachments=files)
        else:
            files = [
                discord.File(player_hand_image_path, filename=f'player_hand_{ctx.author.id}.png'),
                discord.File(dealer_hand_image_path, filename=f'dealer_hand_{ctx.author.id}.png')
            ]
            game['message'] = await ctx.send(embed=embed, files=files)
            await game['message'].add_reaction('🇭')
            await game['message'].add_reaction('🇸')
            # Schedule message deletion
            await game['message'].delete(delay=self.delete_delay)

        # Clean up temporary files
        os.remove(player_hand_image_path)
        os.remove(dealer_hand_image_path)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if user.id in self.games and self.games[user.id]['message'].id == reaction.message.id:
            if reaction.emoji == '🇭':
                await self.hit(reaction.message, user, reaction.emoji)
            elif reaction.emoji == '🇸':
                await self.stay(reaction.message, user, reaction.emoji)

    async def hit(self, message, user, emoji):
        game = self.games[user.id]
        deck = self.create_deck()
        player_hand = game['player_hand']
        player_hand.append(deck.pop())

        await self.show_hands(game['ctx'])

        if self.calculate_hand_value(player_hand) > 21:
            await self.end_game(user, won=False)
        else:
            await self.show_hands(game['ctx'])
        await message.remove_reaction(emoji, user)

    async def stay(self, message, user, emoji):
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

        # Remove the user's reaction
        await message.remove_reaction(emoji, user)

    async def end_game(self, user, won):
        game = self.games.pop(user.id)
        player_hand = game['player_hand']
        dealer_hand = game['dealer_hand']
        player_hand_str = ' '.join([f'{value} of {suit}' for value, suit in player_hand])
        dealer_hand_str = ' '.join([f'{value} of {suit}' for value, suit in dealer_hand])
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        # Create final hand images
        player_hand_image = self.create_hand_image(player_hand)
        dealer_hand_image = self.create_hand_image(dealer_hand)

        player_hand_image_path = os.path.join(self.temp_path, f'player_hand_{user.id}.png')
        dealer_hand_image_path = os.path.join(self.temp_path, f'dealer_hand_{user.id}.png')

        player_hand_image.save(player_hand_image_path)
        dealer_hand_image.save(dealer_hand_image_path)

        if won:
                        # self.high_scores[user.id] = self.high_scores.get(user.id, 0) + 1
            result = f'You win! Your hand: {player_hand_str} (Total: {player_value}),\n Dealer\'s hand: {dealer_hand_str} (Total: {dealer_value})\u200b\n\u200b\n'
        else:
            result = f'You lose! Your hand: {player_hand_str} (Total: {player_value}),\n Dealer\'s hand: {dealer_hand_str} (Total: {dealer_value})\u200b\n\u200b\n'

        embed = discord.Embed(title="Blackjack", description=result)
        embed.set_image(url=f'attachment://player_hand_{user.id}.png')
        embed.set_footer(text='\u200b\n\u200b\nTHIS MESSAGE WILL SELF-DESTRUCT IN 90 SECONDS')

        files = [
            discord.File(player_hand_image_path, filename=f'player_hand_{user.id}.png'),
            discord.File(dealer_hand_image_path, filename=f'dealer_hand_{user.id}.png')
        ]

        await game['message'].edit(embed=embed, attachments=files)
        await game['message'].delete(delay=self.delete_delay)

        os.remove(player_hand_image_path)
        os.remove(dealer_hand_image_path)

    # @commands.command(name='highscores')
    # async def highscores(self, ctx):
    #     """Show the high score list."""
    #     high_score_list = sorted(self.high_scores.items(), key=lambda x: x[1], reverse=True)
    #     high_score_str = '\n'.join([f'{self.bot.get_user(user_id)}: {score}' for user_id, score in high_score_list])
    #     message = await ctx.send(f'High Scores:\n{high_score_str}')
    #     # Schedule high scores message deletion
    #     await message.delete(delay=self.delete_delay)

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
