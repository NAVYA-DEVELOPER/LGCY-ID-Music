from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from VCBot.handlers import skip_current_song, skip_item
from VCBot.queues import QUEUE, clear_queue

@Client.on_message(contact_filter & filters.command(['skip', 'next', 'n'], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
   chat_id = m.chat.id
   if len(m.command) < 2:
      op = await skip_current_song(chat_id)
      if op==0:
         await m.reply("**π΅ππππππ ππ πΊππππππππ...**")
      elif op==1:
         await m.reply("πΈππππ ππ π¬ππππ, π³ππππππ π½ππππ πͺπππ...")
      elif op==2:
         await m.reply(f"**Some Error Occurred** \n`Clearing the Queues and Leaving the Voice Chat...`")
      else:
         await m.reply(f"**Skipped β­** \n**Now Playing** - [{op[0]}]({op[1]}) | `{op[2]}`", disable_web_page_preview=True)
   else:
      skip = m.text.split(None, 1)[1]
      OP = "**Removed the following songs from Queue:-**"
      if chat_id in QUEUE:
         items = [int(x) for x in skip.split(" ") if x.isdigit()]
         items.sort(reverse=True)
         for x in items:
            if x==0:
               pass
            else:
               hm = await skip_item(chat_id, x)
               if hm==0:
                  pass
               else:
                  OP = OP + "\n" + f"**#{x}** - {hm}"
         await m.reply(OP)        
      
@Client.on_message(contact_filter & filters.command(['end', 'stop', 'X', 'e'], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         await m.reply("**πππ πππππ½ππ ππΌπ πΏπππΎπππππΎπππΏ ππππ πππΏππ πΎππΌπ π€........**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("π΅ππππππ ππ πΊππππππππ...")
   
@Client.on_message(contact_filter & filters.command(['pause', 'wait', 'ruko'], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.pause_stream(chat_id)
         await m.reply("**Paused Streaming βΈοΈ**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("π΅ππππππ ππ πΊππππππππ...")
      
@Client.on_message(contact_filter & filters.command(['resume', 'r', 'run' , 'chalo'], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.resume_stream(chat_id)
         await m.reply("**Resumed Streaming βΆ**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("π΅ππππππ ππ πΊππππππππ...")
