import discord
from ext import commands
import asyncio 

red = '\N{LARGE RED CIRCLE}'
blue = '\N{LARGE BLUE CIRCLE}'
blank = '\N{MEDIUM BLACK CIRCLE}'


class ConnectFour:


    def __init__(self, bot):
        self.bot = bot
    
    @staticmethod
    def grid_maker():
        rows = 7
        cols = 7
        grid = []
        for i in range(rows):
            line = []
            for value in range(cols):
                line.append(blank)
            grid.append(line)
        return grid


    async def get_move(self, base, player):

        def move_check(message):
            if message.author == player:
                return True


        msg = await self.bot.wait_for_message(timeout=60, 
                                              channel=base.channel, 
                                              check=move_check)
        while msg:
            if msg.content.isdigit():
                print('yes')
                if int(msg.content) >= 1 and int(msg.content) <= 7:
                    ret = int(msg.content) - 1
                    await asyncio.sleep(0.2)
                    await self.bot.delete_message(msg)
                    return ret
                else:
                    to_del = await self.bot.send_message(base.channel, 'Enter a valid number {}'.format(player.mention))
                    await asyncio.sleep(0.2)
                    await self.bot.delete_messages([msg, to_del])
            else:
                if msg.content.strip().lower() == 'give up':
                    return None
                to_del = await self.bot.send_message(base.channel, 'You have to enter an integer {}'.format(player.mention))
                await asyncio.sleep(0.1)
                await self.bot.delete_messages([msg, to_del])

            msg = await self.bot.wait_for_message(timeout=60, 
                                                  channel=base.channel, 
                                                  check=move_check)
        print('NO')
        return None


    async def player_input(self, base, grid, colour, player):
        to_del = await self.bot.send_message(base.channel, 'Enter a move {}'.format(player.mention))
        move = await self.get_move(base, player)
        await self.bot.delete_message(to_del)
        while move is not None:
            for i in range(len(grid)):
                if grid[i][move] == blank:
                    grid[i][move] = colour
                    pos = [i,int(move)]
                    return [grid, pos]
            to_del = await self.bot.send_message(base.channel,"Column Full! Try another Column")
            move = await self.get_move(base, player)
            await self.bot.delete_message(to_del)
        return False


    async def display_grid(self, base, grid):
        fmt = ''
        for i in reversed(grid):
            fmt += ''.join(i)+' \n'
        numbers = ':one::two::three::four::five::six::seven:'
        fmt += numbers
        await self.bot.edit_message(base, fmt)



    async def start_game(self, ctx, base, p1, p2):
        grid = self.grid_maker()
        cycles = int(len(grid)*len(grid[0])/2)
        for i in range(cycles):
            # Player 1

            await self.display_grid(base, grid)
            move = await self.player_input(base, grid, red, p1)
            if not move:
                await self.bot.say('**{}** wins the game! **{}** gave up!'.format(p2.name, p1.name))
                break
            if self.win_condition(move[1], move[0], red):
                await self.display_grid(base, grid)
                await self.bot.say('**{}** wins the game! 4 in a row!'.format(p1.name))
                break

            # Player 2

            await self.display_grid(base, grid)
            move = await self.player_input(base, grid, blue, p2)
            if not move:
                await self.bot.say('**{}** wins the game! **{}** gave up!'.format(p1.name, p2.name))
                break
            if self.win_condition(move[1], move[0], blue):
                await self.display_grid(base, grid)
                await self.bot.say('**{}** wins the game! 4 in a row!'.format(p2.name))
                break

        
        
    @commands.command(pass_context=True, aliases=['4row'])
    async def four_row(self, ctx, player: discord.Member):
        p1, p2 = ctx.message.author, player
        base = await self.bot.say('**{}** has challenged **{}** to a connect-four duel!'.format(p1.name, p2.name))
        await asyncio.sleep(3)
        await self.start_game(ctx, base, p1, p2)

    @staticmethod
    def win_condition(coordinate, grid, colour):
        row_num = coordinate[0]
        col_num = coordinate[1]

        horizontal_counter = 0
        horizontal_row = ''.join(grid[row_num])
        for value in horizontal_row:
            if value == colour:
                horizontal_counter += 1
            else:
                horizontal_counter = 0
            if horizontal_counter == 4:
                return True
        vertical_counter = 0
        for i in range(row_num+1):
            if grid[i][col_num] == colour:
                vertical_counter += 1
            else:
                vertical_counter = 0
            if vertical_counter == 4:
                return True
        diagonal_counter_one = 0
        diagonal_counter_two = 0
        for num in range(4):
            try:
                if grid[row_num-num][col_num+num] == colour:
                    diagonal_counter_one += 1
            except:
                pass
            try:
                if grid[row_num-num][col_num-num] == colour:
                    diagonal_counter_two += 1
            except:
                pass

        if diagonal_counter_one == 4:
            return True
        if diagonal_counter_two == 4:
            return True
        return False

        
    
    
def setup(bot):
    bot.add_cog(ConnectFour(bot))


            
    


    

    
