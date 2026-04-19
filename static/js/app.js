let currentPublicKey = null;
let currentPrivateKey = null;


// ================= KEY =================
async function generateKey() {
    const resultEl = document.getElementById("key-result");
    resultEl.innerHTML = "";

    const A_input = document.getElementById("A").value.trim();
    const u_input = document.getElementById("u").value.trim();
    const M_input = document.getElementById("M").value.trim();

    if (!A_input || !u_input || !M_input) {
        resultEl.innerHTML = `<span class="error">Please fill out all fields</span>`;
        return;
    }

    const A = A_input.split(",").map(x => parseInt(x.trim()));
    const u = parseInt(u_input);
    const M = parseInt(M_input);

    if (A.some(isNaN) || isNaN(u) || isNaN(M)) {
        resultEl.innerHTML = `<span class="error">Invalid number format</span>`;
        return;
    }

    try {
        const res = await fetch("/api/generate-key", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ A, u, M })
        });

        const data = await res.json();

        if (!res.ok) {
            resultEl.innerHTML = `<span class="error">${data.message}</span>`;
            return;
        }

        currentPublicKey = data.public_key;
        currentPrivateKey = data.private_key;

        resultEl.innerText =
            "S: " + data.public_key.S.join(", ") +
            " | M: " + data.public_key.M;

    } catch {
        resultEl.innerHTML = `<span class="error">Server error</span>`;
    }
}


// ================= ENCRYPT =================
async function encrypt() {
    const bitsEl = document.getElementById("encrypt-bits");
    const cipherEl = document.getElementById("encrypt-cipher");

    bitsEl.innerText = "";
    cipherEl.innerText = "";

    if (!currentPublicKey) {
        cipherEl.innerHTML = `<span class="error">Generate key first</span>`;
        return;
    }

    const P = document.getElementById("enc-P").value.trim().toUpperCase();

    if (!P) {
        cipherEl.innerHTML = `<span class="error">Enter plaintext</span>`;
        return;
    }

    try {
        const res = await fetch("/api/encrypt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                S: currentPublicKey.S,
                M: currentPublicKey.M,
                P: P
            })
        });

        const data = await res.json();

        if (!res.ok) {
            cipherEl.innerHTML = `<span class="error">${data.message}</span>`;
            return;
        }

        bitsEl.innerText = "Bits: " + data.bits.join("");
        cipherEl.innerText = "Cipher: " + data.cipher.join(", ");

        document.getElementById("dec-C").value =
            data.cipher.join(", ");

    } catch {
        cipherEl.innerHTML = `<span class="error">Server error</span>`;
    }
}


// ================= DECRYPT =================
async function decrypt() {
    const cphayEl = document.getElementById("decrypt-cphay");
    const bitsEl = document.getElementById("decrypt-bits");
    const textEl = document.getElementById("decrypt-text");

    cphayEl.innerText = "";
    bitsEl.innerText = "";
    textEl.innerText = "";

    if (!currentPrivateKey || !currentPublicKey) {
        textEl.innerHTML = `<span class="error">Generate key first</span>`;
        return;
    }

    const C_input = document.getElementById("dec-C").value.trim();

    if (!C_input) {
        textEl.innerHTML = `<span class="error">Enter cipher</span>`;
        return;
    }

    const C = C_input.split(",").map(x => parseInt(x.trim()));

    if (C.some(isNaN)) {
        textEl.innerHTML = `<span class="error">Invalid cipher format</span>`;
        return;
    }

    try {
        const res = await fetch("/api/decrypt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                A: currentPrivateKey.A,
                u: currentPrivateKey.u,
                M: currentPublicKey.M,
                C: C
            })
        });

        const data = await res.json();

        if (!res.ok) {
            textEl.innerHTML = `<span class="error">${data.message}</span>`;
            return;
        }

        cphayEl.innerText = "C': " + data.c_phay.join(", ");
        bitsEl.innerText = "Bits: " + data.bits.join("");
        textEl.innerText = "Plaintext: " + data.text;

    } catch {
        textEl.innerHTML = `<span class="error">Server error</span>`;
    }
}