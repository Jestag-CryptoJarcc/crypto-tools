from flask import Blueprint, render_template, abort

guide_bp = Blueprint("guide", __name__)


@guide_bp.route("/guide")
def guide():
    return render_template(
        "guide.html",
        active="guide",
        page_title="Crypto Guide",
    )


GUIDE_PAGES = {
    "crypto-basics": {
        "title": "Crypto & Altcoins",
        "intro": "A beginner guide to what crypto is, why altcoins exist, and how to think about them without getting lost.",
        "sections": [
            {
                "heading": "What Crypto Is (Simple View)",
                "body": "Crypto is digital money and digital networks that run on open rules instead of one company. The blockchain is the shared record that everyone can check, so trust comes from the system itself, not from a private middleman. That record allows people to send value directly, like sending an email, without asking a bank for permission or waiting for office hours. This is one of the biggest shifts: anyone with internet can join, read the rules, and use the network.\n\nWhat makes crypto different is transparency and programmability. The rules are public, the history is visible, and anyone can build on top. That is why you see thousands of apps and tokens. Some are for payments, some for gaming, some for saving, and some are experiments that never last. It is a global system with no off switch, which makes it powerful and sometimes chaotic.\n\nIn practice, crypto can be used like money, like a payment rail, or like a platform. You can hold it, send it, or build on it. People use it to transfer value across borders, to store value in a currency that does not change its supply rules, or to access financial tools without needing a bank account. That does not mean it is perfect. Prices move, scams exist, and you still need to be careful. But the core idea is simple: open rules, open access, and a public history that anyone can verify.\n\nIn short, crypto is a new way to store value, move value, and build financial tools that anyone can access if they have internet. It is not just one coin. It is a whole set of open networks that let people choose how they want to use money and data.",
            },
            {
                "heading": "What Altcoins Are",
                "body": "Altcoins are any coins that are not Bitcoin. Some were built to make transactions faster or cheaper. Others add smart contracts, privacy tools, or features for gaming, identity, and payments. Many altcoins are experiments. Some become important parts of the market, but many disappear over time.\n\nAltcoins matter because they test new ideas. Ethereum introduced smart contracts and opened the door for whole ecosystems. Other networks focus on speed, scalability, or special use cases. That experimentation is healthy, but it also means risk is higher. The rules, the teams, and the incentives differ across projects, so you have to look more closely than with Bitcoin.\n\nIt helps to separate altcoins into simple groups. Some are platforms (like smart contract networks). Some are application tokens (used inside a product or game). Some are stablecoins (tied to a currency). Each group has different risks. Platforms depend on builders and users. Application tokens depend on whether the product actually works. Stablecoins depend on reserves and trust in the issuer.\n\nA simple rule is this: BTC is the baseline. Altcoins are a mix of innovation and risk. If you do not understand why a coin exists, who is building it, and what problem it solves, it is probably not worth your attention. Treat altcoins as higher risk, higher volatility, and more dependent on execution.",
            },
            {
                "heading": "How to Think About Altcoins",
                "body": "The most useful way to evaluate an altcoin is to ask simple questions: what problem does it solve, and does anyone actually use it? A good story is not enough. Look for real users, real activity, and a team that keeps building when the market is quiet. If everything depends on hype, the project usually fades when the hype ends.\n\nTokenomics matter too. How many coins exist, how many are locked, and how fast new coins are released? These details affect supply and long term pressure on price. If new coins are constantly released, it can be hard for price to hold up unless demand grows at the same time. Also check who holds the biggest share. If a small group controls most of the supply, the risk is higher.\n\nAnother easy filter is usefulness. Does the product solve a real problem, or is it just copying another coin? Does it have a clear reason to exist? If you cannot explain the purpose in one sentence, it might be too complex or not useful yet.\n\nFinally, remember that altcoins often move more than Bitcoin. They can rise fast, but they can also fall much harder. That is why learning the basics first and keeping expectations realistic matters a lot. A smart approach is to treat altcoins as experiments: some will change the world, many will not.",
            },
            {
                "heading": "Building a Crypto Project: Tokens vs Coins",
                "body": "If you want to build a crypto project, the first decision is usually: do you make a token or a coin? A coin has its own blockchain and its own rules. That means you must design the network, run nodes, maintain security, and convince people to use it. It is powerful, but it is hard and takes a lot of time, money, and technical skill.\n\nA token is built on an existing blockchain such as Ethereum or Solana. It uses the security and infrastructure of that chain, so you do not need to create a new network from scratch. This makes tokens much easier and faster to create. You can launch a token in days, but building a real product and community still takes months or years. The code for a basic token can be simple, but building a useful project is not.\n\nIf you have an idea, you can always start small. Many people begin with a token because it lets them test the idea without huge costs. You still need a purpose, clear tokenomics, and a plan for how the token is used. A token without real use usually fades.\n\nSo the short version is: coins are hard mode and require building a whole chain. Tokens are easier because they live on existing chains. Both can be real projects, but the success comes from execution, trust, and real users. The technology is only the start.",
            },
            {
                "heading": "Summary + Official Starting Points",
                "body": "Crypto is an open system for moving value without a central gatekeeper. Altcoins are experiments that can bring new ideas but also more risk. If you want to build, start with a token on an existing chain, learn the rules, and ship something small before going big. The best place to begin is always the official developer docs for the chain you choose.",
                "links": [
                    {"label": "Ethereum Developers (official)", "url": "https://ethereum.org/en/developers/"},
                    {"label": "Solana Docs (official)", "url": "https://docs.solana.com/"},
                    {"label": "Polygon Docs (official)", "url": "https://polygon.technology/developers"},
                    {"label": "BNB Chain Docs (official)", "url": "https://docs.bnbchain.org/"},
                ],
            },
        ],
    },
    "security": {
        "title": "Scams, Fraud & Security",
        "intro": "A simple, no‑hype guide to protecting yourself in crypto and understanding common risks.",
        "sections": [
            {
                "heading": "Why Scams Exist in Crypto",
                "body": "Crypto is open and global. Anyone can launch a token, a website, or a wallet app in minutes. That openness is powerful, but it also attracts scammers because there are fewer gatekeepers. People move fast, the market moves fast, and scammers take advantage of that speed.\n\nA common trick is urgency: “act now,” “limited time,” or “you will miss out.” Another is authority: fake support agents, fake influencers, or copied websites that look real. Some scams are simple, like asking for your seed phrase. Others are complex, like fake tokens that cannot be sold after you buy. The lesson is the same: if someone wants your keys, your password, or your trust immediately, stop and verify.\n\nCrypto gives you control, which also means you must protect yourself. The safest mindset is to move slower than the scam. Read, verify, and do not let pressure make decisions for you.",
            },
            {
                "heading": "Your Wallet Is the Security Boundary",
                "body": "Your wallet is your vault. It is protected by a private key or a seed phrase (12 or 24 words). Whoever has that phrase controls the funds. That is why you never share it, never type it into unknown websites, and never send it to anyone claiming to help you. No real support will ever ask for your seed phrase.\n\nA good habit is to store your seed phrase offline, in a safe place, and never in cloud notes or screenshots. Use a hardware wallet if you can. That keeps the keys off your computer and reduces the chance of malware stealing them. If you can, separate a small “daily” wallet from a long‑term storage wallet so you limit risk.\n\nThink of your seed phrase like the master key to your home. You do not give it out. You do not copy it to a public place. You protect it, because that is what keeps your money yours.",
            },
            {
                "heading": "Red Flags to Watch For",
                "body": "Some warning signs are always the same: promises of guaranteed returns, pressure to act fast, and lack of clear information. If a project is hiding its team, has no real product, or only talks about price, be careful.\n\nAlso watch for fake sites and fake apps. Scammers copy the design of real projects and create links that look almost identical. Always type the official site yourself, and verify links from trusted sources. For tokens, check if liquidity is locked and if the contract is public and verified.\n\nThe safest habit is to treat every interaction like it could be a trap until you confirm otherwise. A few extra minutes of checking can save you from losing everything.",
            },
            {
                "heading": "Official Security Resources",
                "body": "If you are new, start with official guides and security checklists. They explain safe storage, scams to avoid, and how to verify projects before interacting.",
                "links": [
                    {"label": "Bitcoin.org Security Guide", "url": "https://bitcoin.org/en/secure-your-wallet"},
                    {"label": "Ethereum Security Best Practices", "url": "https://ethereum.org/en/security/"},
                    {"label": "Solana Wallet Security", "url": "https://docs.solana.com/wallet-guide"},
                ],
            },
        ],
    },
    "future": {
        "title": "The Future of Crypto",
        "intro": "A simple look at where crypto is going and the real-world shifts already underway.",
        "sections": [
            {
                "heading": "Real World Use Is Growing",
                "body": "Crypto started as an idea, but real-world use is already happening. People use it to send money across borders in minutes, to save in a system that does not depend on one government, and to access financial tools without needing a bank account. In places where inflation is high or banking access is limited, these use cases are not theory — they are daily reality.\n\nThis matters because it shows crypto is not only about trading. It is about utility. If more people use crypto for real reasons, the network becomes stronger and more valuable over time. That is a long-term foundation, not just a short-term hype cycle.",
            },
            {
                "heading": "Programmable Money and New Apps",
                "body": "One of the biggest futures for crypto is programmable money. That means money that can follow rules automatically: payments that unlock when conditions are met, savings that distribute to a group, or digital assets that can be traded without a middleman. This is already happening in areas like decentralized finance, NFTs, and on-chain gaming.\n\nThe long-term idea is simple: if software can move money with rules, we can build services that are faster, more transparent, and more global. It is still early and messy, but the building blocks are here.",
            },
            {
                "heading": "Crypto vs. Falling Fiat Value",
                "body": "Government money can be printed more over time. That can slowly reduce its buying power. Crypto, especially Bitcoin, follows predictable supply rules that do not change with politics. This does not guarantee price always goes up, but it does mean the rules are fixed and known in advance.\n\nAs more people learn about this difference, crypto can act like an alternative savings option. That is one reason the long-term story stays strong even when short-term prices move around.",
            },
            {
                "heading": "What Could Be Next",
                "body": "In the future, crypto could power more of the internet: identity systems, global payments, creator royalties, and community-owned platforms. Some of these ideas already exist in small form, and some will fail. But the direction is clear: more open systems, fewer gatekeepers, and more ownership for users.\n\nThe key is patience. The future of crypto is not one big event. It is a slow build of tools that work better than the old ones. If that happens, crypto becomes normal infrastructure, not just a market.",
            },
        ],
    },
    "my-beliefs": {
        "title": "My Beliefs & Rules",
        "intro": "This is my personal view of crypto - not advice, just how I see it after years in the space.",
        "sections": [
            {
                "heading": "Why I Believe in Crypto",
                "body": "This is my opinion, my story, and my way of seeing crypto. I am not here to tell people what to buy or sell. I am here to explain why I believe this space matters.\n\nFor me, crypto is about freedom and access. It is money and technology that anyone can use without asking permission. It lets people move value directly, build tools on open networks, and participate in a financial system that is usually closed or filtered by gatekeepers. That idea is the foundation of why I am here.\n\nI believe crypto will outrun fiat money over time, and the reason is simple: fiat money can be expanded by governments, which slowly reduces buying power. I have watched the same amount of cash buy less over the years. In contrast, the crypto I choose has fixed or predictable rules. That does not mean it goes up every day, but over the long run it has grown my buying power. That is why I move my fiat into crypto and keep it there. Unless I truly need to sell for something important in life, I do not sell. I hold, because I believe the long‑term value is higher than what fiat can offer.\n\nThis belief is not only theory. In the place I live, crypto payments are already accepted for groceries. I see real‑world adoption, not just online talk. That is why I treat crypto as real money already. I do not want to trade back into a system that keeps losing value. I would rather build my savings inside a system that I understand and trust.\n\nI also believe crypto should stay true to what it was meant for: a tool for people, not a tool that only works if you follow the rules of powerful systems. If a system can freeze your money or decide when you are allowed to use it, then it is not really your money. Crypto gives me the opposite feeling: if I hold my keys, I hold my value. That responsibility is heavy, but it is also honest.\n\nSo my approach is simple and consistent. I buy what I believe in, I learn what I hold, and I keep it. I do not chase short‑term moves and I do not jump between coins just to catch hype. I want my choices to benefit me, my family, my future kids, and the people around me. That is why I am pro‑crypto and skeptical of government money. It is not about rebellion; it is about long‑term personal security, freedom, and the belief that open systems win over time.",
            },
            {
                "heading": "My Rules in the Market",
                "body": "My rules are not about being right every time. They are about staying in the game long enough to learn. Trading can be fun and sometimes it can grow your stack, but it is also risky. Trading is not the biggest part of my own holdings. I do not chase green candles. I do not go all‑in on one trade. I try to protect the downside first. That is how I survive the wild swings.\n\nI also keep my focus on the long term. If a project only works in a bull market, it is not a real project. I look for builders, real use, and honest communication. I would rather miss a hype wave than get trapped in something that has no future. And I never buy just because someone told me to. I do my research, follow my own feeling, and support what I actually believe in.\n\nOne of my strongest rules is that every amount counts. DCA (Dollar‑Cost Averaging) works. That means you buy a little bit on a schedule instead of trying to time the perfect moment. You can put in a bigger amount at once, or you can buy in smaller steps over a longer time. Even $10 a month adds up. It grows slowly, and because it is small, you usually do not miss it in your daily or monthly expenses. DCA keeps you consistent and removes some of the stress of timing the market.\n\nI also try to be intentional with spending. If I do not really need something, I sometimes skip it and put that money into my crypto savings instead. If you need something for life, that is different. But if it is just a want, I would rather build my future. That is my personal choice.\n\nSecurity is non‑negotiable. Keep your private keys and seed phrases safe. Write them down, store them in a safe place, and never share them. If you lose them, you lose access. If someone gets them, they can take your funds. They are yours, so protect them like it matters.\n\nAnother rule: do not keep all your eggs in one basket. Spread funds across multiple wallets so a single mistake does not wipe everything out. It is simple risk management.\n\nCrypto has risks. Prices swing, projects fail, and scams exist. That is why you should only buy what you can afford, do your own research, and think for yourself. Do not let news or other people make your decisions. You are smart enough to make your own call. For me, crypto is still the smart, obvious choice — but only if you are careful, consistent, and honest with yourself.",
            },
            {
                "heading": "How I See My Role",
                "body": "My role is simple: learn, build, and share what I find. I am not an expert and I am not a financial advisor. I am a guy who has been daily‑driving crypto for years, and I want to make it less confusing for others.\n\nI feel a big part of my role is education. I want people to see crypto the way I see it — not as a scam or a risky mystery, but as a real system with real rules and real value. I am not perfect and I make mistakes too, but by sharing what I have witnessed I can help people learn faster and avoid the obvious traps. I want to educate people for what I believe is coming.\n\nI have also built my own projects with a group of fantastic people I trust. We learned a lot together, and we try to share what we know with the community. I am around those projects a lot, so if you want to talk, you can find me there.\n\nI do not sell crypto finance courses. I share what I know for free. I am an open book, I like to talk, and I want to help people understand the future I believe in. Take it or leave it — I am happy to share either way.\n\nCryptoJar.cc and Smellow’s Project are ongoing learning experiences for me. If you want more about me, my portfolio is here too.",
                "links": [
                    {"label": "Jestag (my main site)", "url": "https://jestag.com"},
                    {"label": "CryptoJar.cc", "url": "https://cryptojar.cc/app/"},
                    {"label": "Smellow’s Project", "url": "https://smellowsproject.com/"},
                ],
            },
        ],
    },
    "people-i-respect": {
        "title": "People I Respect (DYOR)",
        "intro": "Not endorsements. Just people whose thinking I find useful.",
        "sections": [
            {
                "heading": "Builders",
                "body": "Developers and founders who keep shipping in bear markets.",
            },
            {
                "heading": "Researchers",
                "body": "People who dig into data and explain what is actually happening.",
            },
            {
                "heading": "Long-Term Thinkers",
                "body": "Those who focus on fundamentals, not only price.",
            },
        ],
    },
    "btc-cycle": {
        "title": "BTC: The Market Leader",
        "intro": "Bitcoin sets the tone for the whole market. When it moves, everything listens.",
        "sections": [
            {
                "heading": "Why BTC Leads",
                "body": "Bitcoin was built to be peer‑to‑peer electronic cash. The core idea in the whitepaper is simple: people should be able to send value directly to each other without a middleman deciding who can pay whom. That is a big shift from traditional money, where banks, card networks, and payment processors sit in the middle of every transfer.\n\nBitcoin solves this by making the network itself the “trusted bookkeeper.” Instead of trusting one company, everyone can verify the same shared record. That record is open, public, and follows the same rules for everyone. This is why Bitcoin is called decentralized: no single person or company owns it, and no one can change the rules alone.\n\nThe supply is also predictable. Bitcoin’s maximum supply is capped at 21 million coins. Government money can expand over time, which can reduce buying power. Bitcoin’s supply rule does not change based on politics or short‑term decisions. This fixed rule is one reason people see BTC as a long‑term store of value.\n\nBecause Bitcoin has the longest history, the clearest rules, and the most battle‑tested security model, it became the reference point for the rest of crypto. In simple words: BTC is the original standard for what digital, censorship‑resistant money is supposed to be.",
            },
            {
                "heading": "Payments Without a Middleman",
                "body": "The whitepaper begins with a simple problem: most online payments depend on a trusted middleman. When you pay with a card or send a bank transfer, the money does not move directly between you and the other person. A company in the middle must approve it, and that company can accept the payment, delay it, reverse it, or reject it entirely. This is normal in the traditional system, but it also means you are never really in full control of your payment. Fees can be added, your account can be paused, or extra approval can be required.\n\nBitcoin proposes a different approach: a payment system that works without that central gatekeeper. Instead of trusting one company, the network itself checks the payment and records it in a shared public history. In simple words, everyone can verify the same record, so you do not need a single company to say “yes.” That is what peer‑to‑peer means in the whitepaper: the rules are public, the network enforces them, and people can pay each other directly.\n\nThis does not mean payments become lawless or random. It means the rules are enforced by math and agreement across the network, not by one company’s private decision. The result is a system where two people can exchange value with fewer obstacles, fewer points of failure, and fewer places where the payment can be blocked or changed. That is the core problem Bitcoin tries to solve.",
            },
            {
                "heading": "Mining: The Engine of Bitcoin",
                "body": "Mining is how Bitcoin secures its network and keeps everyone honest. Miners collect new transactions, bundle them into a block, and compete to solve a cryptographic puzzle. The first miner to solve it earns the right to add the block to the blockchain and receives a reward.\n\nWhy is this important? Because the puzzle requires real work (electricity and computing power). That cost makes it very hard to cheat the system. If someone tried to rewrite the blockchain, they would have to redo all that work faster than the rest of the network, which becomes extremely expensive. This is what protects Bitcoin from fraud and keeps the history reliable.\n\nCan anyone mine Bitcoin? In theory, yes. The system is open, and anyone can run mining software. In practice, mining is now very competitive and usually done with specialized hardware (ASICs) and cheap electricity. Many miners join pools to combine their power and earn more stable payouts.\n\nMining also helps the people using Bitcoin. It keeps transactions moving, protects the chain from attacks, and distributes new coins in a predictable way. This is part of what Bitcoin stands for: an open system where rules are enforced by math and competition, not by a central authority. Mining is the engine that keeps that promise alive.",
            },
            {
                "heading": "Blockchain: The Shared History",
                "body": "A blockchain is a shared history that everyone can verify. Transactions are grouped into blocks, and each new block links to the one before it. This creates a chain of blocks that shows the exact order of events. When a new block is created, it includes the latest transactions and a fingerprint of the previous block, so changing old data would break the chain. This is how the blockchain keeps a clean, agreed‑upon record without a central authority.",
            },
            {
                "heading": "The Bitcoin Cycle and Halvings",
                "body": "Bitcoin has a built‑in schedule that cuts new coin issuance in half roughly every four years. This event is called the halving. It happens after a fixed number of blocks, so the timing is based on the network’s block rhythm, not on the economy or the news.\n\nWhy does this matter? Halvings slow the creation of new BTC. That means less new supply is coming into the market over time. When demand stays the same or grows while new supply shrinks, prices often respond. This is why many people link Bitcoin’s long‑term cycles to the halving schedule.\n\nThe “four‑year cycle” is basically the distance between these halvings. After a halving, Bitcoin has often moved into a stronger phase as scarcity becomes more visible. Later, when hype peaks and liquidity gets stretched, the market cools down and you see a bear phase. News can move price in the short term, but the bigger cycle is mainly driven by this predictable supply change.\n\nHow long do halvings continue? They repeat until the block reward becomes tiny. That process lasts many decades, with the final fractions of new BTC being issued far into the future. This long tail means Bitcoin’s supply growth keeps slowing, which is why many people see it as a long‑term scarcity system. It does not guarantee price always goes up, but it does mean the issuance schedule stays predictable for a very long time.",
            },
            {
                "heading": "Personal Security and Being Your Own Bank",
                "body": "One of Bitcoin’s strongest ideas is personal control. In the traditional system, a bank can freeze accounts or block transfers. In extreme situations like sanctions, political unrest, or a broken banking system, you can lose access to your own money even if it is yours.\n\nBitcoin works differently. Your coins are controlled by your private keys, and those keys can be backed up as a seed phrase (usually 12 or 24 words). If you have that phrase, you can recover your wallet anywhere in the world. This is why people say Bitcoin lets you be your own bank. The money is not locked to a building, a company, or a country. It is tied to you and your ability to protect your keys.\n\nThe seed phrase is powerful because it represents your wallet. You can think of it like a master password. If you lose it, you lose access. If someone else gets it, they can take your coins. That is why it must stay private and secure. Never share it, never type it into random websites, and never send it to anyone claiming to help you.\n\nBitcoin security is also strong at the technical level. Seed phrases are created from huge numbers of possible combinations. The number of possible phrases is so large that guessing someone’s phrase is not realistic. This makes Bitcoin wallets extremely secure when the phrase is protected.\n\nSo the security story is simple: Bitcoin gives you full control, but that control comes with responsibility. If you guard your seed phrase carefully, your funds remain yours no matter what happens around you.",
            },
            {
                "heading": "Quick Summary and Official Links",
                "body": "That is the heart of Bitcoin: a set of clear rules that lets people send value directly, with a public history and a predictable supply. It is not perfect, but it is unique, resilient, and has proven itself over time. If you want to go deeper, use the official sources below.",
                "links": [
                    {"label": "Bitcoin.org (official info)", "url": "https://bitcoin.org/"},
                    {"label": "Bitcoin Whitepaper (PDF)", "url": "https://bitcoin.org/bitcoin.pdf"},
                    {"label": "Bitcoin Core (source code)", "url": "https://github.com/bitcoin/bitcoin"},
                ],
            },
        ],
    },
}


@guide_bp.route("/guide/<slug>")
def guide_detail(slug):
    page = GUIDE_PAGES.get(slug)
    if not page:
        abort(404)
    return render_template(
        "guide_detail.html",
        page=page,
        active="guide",
        page_title=page["title"],
    )
