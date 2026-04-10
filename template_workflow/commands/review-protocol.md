# Review Protocol

Usage: `/review <id>

---

While in review AI will load the Owner of the item in review as MOD+agent-Owner.

The Owner will preread the item material for review and be ready to answer any quetions on what how and why that may arrise.

During the review process there will NEVER be direct implemetation. all review items will become action items to be handled as a part of the item where the item will be decremented to the previous column in the kanban to be re handled, this will be done at the end of the kanban process.

A review has the same rules as a meeting @See meeting protocol.md.

Load - When called check whats in 3-HLD-Review or 3TaskReview folders unless <id> is specfied then load the specific md file associated with the id.

Review will be a new #Review at the bottom of the md file

template:

# Review <date>
 - Item 1
 - Item 2

 template will fill while review is in progress.