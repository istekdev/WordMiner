from termcolor import colored
from eth_utils import keccak
import requests
import json
import time
import os

difficulty = 0
target = 0

if os.path.exists("chain.json"):
  with open("chain.json", "r") as r:
    read = json.load(r)
  if read == {}:
    pass
  else:
    newest = list(read.keys())[-1]
    target = read[newest]["target"]
    difficulty = (2**244 * (2**32 - 1)) // target
else:
  difficulty = 1000000 * 180
  target = (2**224) * ((2**32) - 1) // difficulty

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def mine():
  global target, difficulty
  with open("config.json", "r") as r:
    read = json.load(r)
  c = requests.get(read["endpoint"])
  connect = c.json()
  print(colored(f"Developer: {read["socials"]["developer"]}", "white", attrs=["bold"]))
  print(colored(f"Github: {read["socials"]["github"]}", "white", attrs=["bold"]))
  created = read["socials"]["date_of_creation"]
  local = time.localtime(created)
  date = time.strftime("%Y-%m-%d %H:%M:%S", local)
  print(colored(f"Created: {date}", "white", attrs=["bold"]))
  print("")
  print(colored("Mining Has Begun...", "yellow", attrs=["bold"]))
  version = read["version"]
  max = (2**32) - 1
  start = round(time.time())
  currentword = connect[0]
  timestamp = round(time.time())
  end = 0
  nonce = 0
  while nonce <= max:
    wordhash = keccak(keccak(currentword.encode("utf-8") + target.to_bytes(32, "big") + str(timestamp).encode("utf-8") + nonce.to_bytes(32, "big") + str(end).encode("utf-8") + version.to_bytes(4, "big"))).hex()
    if int(wordhash, 16) <= target:
      print(colored("Word Has Been Mined, Adding To The Blockchain...", "green", attrs=["bold"]))
      end = round(time.time())
      with open("chain.json", "r") as verify:
        ver = json.load(verify)
      if ver == {}:
        block = {
          "version": version,
          "timestamp": timestamp,
          "height": 1,
          "mined": end,
          "word": currentword,
          "nonce": nonce,
          "target": target,
          "wordHash": wordhash,
          "prevHash": "0"*64
        }
        read["1"] = block
        with open("chain.json", "w") as add:
          json.dump(read, add, indent=4)
      else:
        with open("chain.json", "r") as r:
          read = json.load(r)
        prev = list(read.keys())[-2]
        prevHash = read[prev]["wordHash"]
        prevHeight = read[prev]["height"]
        yourHeight = prevHeight + 1
        block = {
          "version": version,
          "timestamp": timestamp,
          "height": yourHeight,
          "mined": end,
          "word": currentword,
          "nonce": nonce,
          "target": target,
          "wordHash": wordhash,
          "prevHash": prevHash
        }
        read[str(yourHeight)] = block
        with open("chain.json", "w") as add:
          json.dump(read, add, indent=4)
    nonce += 1
  if nonce < max:
    print(colored("Nonces Have Been Exhausted - Renewing...", "yellow", attrs=["bold"]))
    mine()
  with open("chain.json", "r") as r:
    read = json.load(r)
  latest = list(read.keys())[-1]
  start = read[latest]["timestamp"]
  end = read[latest]["mined"]
  actual = end - start
  difficulty = difficulty * (180 / actual)
  target = (2**224) * ((2**32) - 1) // difficulty
  clear()
  mine()

def connect():
  print(colored("Establishing A Connection To The API Endpoint...", "yellow", attrs=["bold"]))
  with open("config.json", "r") as r:
    read = json.load(r)
  connect = requests.get(read["endpoint"])
  try:
      word = connect.json()
  except ValueError:
      print(colored("Error - Failed To Connect.", "red", attrs=["bold"]))
      word = None
  print(colored(f"Successfully Connected - Endpoint: {read['endpoint']}", "green", attrs=["bold"]))
  if os.path.exists("chain.json"):
    print(colored("Welcome Back", "green", attrs=["bold"]))
  else:
    print(colored("Generating New Blockchain...", "yellow", attrs=["bold"]))
    with open("chain.json", "w") as new:
      new.write("{}")
    print(colored("Your New Blockchain Has Been Generated", "green", attrs=["bold"]))
  clear()
  mine()

connect()
