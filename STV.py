import csv

#pretty-print dictionaries, may be used for testing
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

#Generate set of eligible emails

candidates = {
	"usga" : ["A", "B", "C"],
	"usgp" : ["A", "B", "C"],
	"sg" : ["A", "B", "C"],
	"dg" : ["A", "B", "C"],
}

#Generate dictionaries of voters format of {email: {1: "first choice", 2: "second choice", ...}}
votes = {
	"usga" : {},
	"usgp" : {},
	"sg" : {},
	"dg" : {},
}

questions = {
	"usga" : "How are you voting for USG of Administration? (1 is first choice, 2 is second choice, etc...)",
	"usgp" : "How are you voting for USG of Personnel? (1 is first choice, 2 is second choice, etc...)",
	"sg" : "How are you voting for Secretary-General? (1 is first choice, 2 is second choice, etc...)",
	"dg" : "How are you voting for Director-General? (1 is first choice, 2 is second choice, etc...)",
}

eligible_emails=set()

with open("eligible_emails.csv") as eligible:
	for email in eligible.readlines():
		eligible_emails.add(email.strip())

#load votes in the previously specified format
with open("votes.csv") as votes_csv:
	vote_data = csv.DictReader(votes_csv)
	for row in vote_data:
		email = row["Email"]

		if email in eligible_emails:

			for key, q in questions.items():
				for candidate in candidates[key]:

					column = f"{q} [{candidate}]"
					ranking = row[column]

					if email not in votes[key]:
						votes[key][email] = {}

					votes[key][email][ranking] = candidate

		else:
			print(f"Ineligible voter with email `{email}`")

for race, rankings in votes.items():
	total_votes = len(rankings)

	counter = {}
	#each candidate starts with 0 votes
	for candidate in candidates[race]:
		counter[candidate] = 0

	#eliminate candidates until only one is left
	while len(counter) > 1:
		print(f"{race} winner: {candidate}")

		#clear votes
		for candidate in counter.keys():
			counter[candidate] = 0

		#cast vote for favorite candidate who is still in the race
		for vote in rankings.values():
			for i in range(1, len(candidates)):
				if vote[str(i)] in counter:
					counter[vote[str(i)]] += 1
					break

		#filter out last place candidates
		min_votes = min(counter.values())
		last = {cand: 0 for cand, votes in counter.items() if votes == min_votes}

		#if there's a tie for last, a decision needs to be made regarding who gets eliminated
		#Votes are recast with only last place candidates, loser is eliminated. If this does not result
		#in a winner, a decision will have to be made by Mykolyk & the Upper Sec as to how this tie
		#should be handled
		if list(counter.values()).count(min(counter.values())) > 1:
			for vote in rankings.values():
				for i in range(1, len(candidates)):
					if vote[str(i)] in last:
						last[vote[str(i)]] += 1
						break

			if list(last.values()).count(min(last.values())) > 1:
				print(f"Tie between candidates in {race} race for last place:")
				print("last:")
				pretty(last)
				print("all:")
				print(list(rankings.values()))

				break

		else:
			#eliminate last place candidate if there is no tie
			cand = list(last.keys())[0]
			del counter[cand]