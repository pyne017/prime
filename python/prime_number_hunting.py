from multiprocessing import Pool, cpu_count
from datetime import datetime
from limit_config import lower_limit, upper_limit
from limit_config import sender_email, receiver_email, password, this_device
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prime_stats import digit_distro,digit_repeat,digit_neighbors,digit_missing
from collections import defaultdict


print("INFO - Always run hunt_primes.py as Python3")
if this_device == "RPI1":
   workers = 1
else:
   workers = cpu_count()
print("Using {0} cpu workers".format(workers))

# Sets lower/upper search space on p where 2** p -1 is a Mersenne prime
if lower_limit % 2 == 0:
   print("Remember that lower limit needs to be odd")
   quit()
print("Starting at {0} for lower_limit {1} and upper_limit {2}\n".format(datetime.now(), lower_limit, upper_limit))
with open("found_primes.txt","a+") as outf:
    outf.write("Starting at {0} for lower_limit {1} and upper_limit {2}\n".format(datetime.now(), lower_limit, upper_limit))

def lucas_lehmer(p):
    s = 4
    m = 2 ** p - 1
    for _ in range(p - 2):
        s = ((s * s) - 2) % m
    if s == 0:
        print("Found prime that is {0} digits long when p={1}".format(len(str(m)), p))
        with open("found_primes.txt","a+") as outf:
            outf.write("*** Found prime of {0} digits when p={1} *** \n".format(len(str(m)), p))
        # Send email alert
        subject = "{0} found prime at p={1}".format(this_device,p)
        body = "{0} found prime at p={1}".format(this_device,p)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(subject))
        text = message.as_string()
    else:
        now = datetime.now()
        print("Eliminated p={0} at {1}".format(p,now))
        with open("found_primes.txt","a+") as outf:
            outf.write("Eliminated p={0} at {1}\n".format(p,now))
        # Send email alert
        subject = "Ipabog on {0} eliminated {1}".format(this_device,p)
        body = "Ipabog on {0} eliminated {1}".format(this_device,p)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(subject))
        text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def is_prime(number):
    i = 3
    while i * i <= number:
        if number % i == 0:
            return False
        i += 2
    return True

candidate_list = []
for i in range(lower_limit, upper_limit, 2):
    if str(i)[-1] != "5":
        candidate_list.append(i)
print("Built candidate list up to {0} of length {1}".format(upper_limit,len(candidate_list)))

prime_results = list()
if this_device == "RPI1":
    for candidate in candidate_list:
        prime_results.append(is_prime(candidate))
else:
    with Pool(workers) as p:
        prime_results = p.map(is_prime, candidate_list)
print("Built prime result list")

#Merge the lists
best_candidates = [candidate_list[i] for i, x in enumerate(prime_results) if x]
print("Built best candidate list of length {0}".format(len(best_candidates)))

# Rank the best candidates
ranked_candidate_list = defaultdict(float)
for candidate in best_candidates:
   num_hits = defaultdict(int)
   for character in str(candidate):
      # Very rare for three instances of the same digit so penalize those numbers harshly
      num_hits[character] += 1
      if num_hits[character] > 2:
          ranked_candidate_list[candidate] += -50
      ranked_candidate_list[candidate] += digit_distro[character]
      ranked_candidate_list[candidate] += digit_repeat[character]
      ranked_candidate_list[candidate] += digit_missing[character]
   for digit_neighbor in digit_neighbors:
      if digit_neighbor in str(candidate):
          ranked_candidate_list[candidate] += digit_neighbors[digit_neighbor]

best_candidates = sorted(ranked_candidate_list.items(),key=lambda x:x[1],reverse=True)
best_candidates = [x[0] for x in best_candidates]
print(sorted(ranked_candidate_list.items(),key=lambda x:x[1],reverse=True)[:10])
print("Ranked best candidates")

if this_device == "RPI1":
    for best_candidate in best_candidates:
         print("Testing",best_candidate,"...")
         lucas_lehmer(best_candidate)
else:
    with Pool(workers) as p:
        p.map(lucas_lehmer, best_candidates)
print("Done")
