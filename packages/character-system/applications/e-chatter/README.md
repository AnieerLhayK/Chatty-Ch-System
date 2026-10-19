# e-Chatter managed releases

ai-workbench is the sole development source. This application directory receives
immutable, independently buildable source snapshots through its manual promotion
command. Fixes return to ai-workbench; do not modify a versioned snapshot.

`candidate.json` selects the latest locally verified candidate; `stable.json`
exists only after all stable acceptance gates pass. Each pointer identifies the
snapshot under versions/, source commit and the shared Windows ZIP SHA-256.
The development and character-system release receipts reference exactly the same
artifact. Binary output stays outside the source repository.

Open the selected version's README for standalone use and build instructions.
Users extract the Windows ZIP and launch without Python/Node; install and log in
to their own supported Agent separately. There are no bundled personal roles.

The public projection explicitly includes only candidate 0.2.0-rc.1 and its
immutable source snapshot. Download it from the Chatty-Ch-System Pre-release
`e-chatter-v0.2.0-rc.1`. Clean Windows 11 and real API Key acceptance remain
unverified; this candidate does not replace a stable release.
