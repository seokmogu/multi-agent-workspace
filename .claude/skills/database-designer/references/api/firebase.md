## Firebase Firestore

**Official Documentation**: https://firebase.google.com/docs/reference/js/firestore
**GitHub**: https://github.com/firebase/firebase-js-sdk
**npm**: `firebase` (v9+ modular)

### Installation

```bash
npm install firebase
```

### Connection Setup

```typescript
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-app.firebaseapp.com",
  projectId: "your-project-id"
}

const app = initializeApp(firebaseConfig)
const db = getFirestore(app)
```

### CRUD Operations

```typescript
import {
  collection,
  doc,
  addDoc,
  getDoc,
  getDocs,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit
} from 'firebase/firestore'

// CREATE (Auto-generated ID)
const docRef = await addDoc(collection(db, 'companies'), {
  name: 'Acme Corp',
  industry: 'Technology'
})

// CREATE (Custom ID)
await setDoc(doc(db, 'companies', 'acme-corp'), {
  name: 'Acme Corp',
  industry: 'Technology'
})

// READ (Single document)
const docSnap = await getDoc(doc(db, 'companies', 'acme-corp'))
if (docSnap.exists()) {
  console.log('Data:', docSnap.data())
}

// READ (Query)
const q = query(
  collection(db, 'companies'),
  where('industry', '==', 'Technology'),
  orderBy('createdAt', 'desc'),
  limit(10)
)
const querySnapshot = await getDocs(q)
querySnapshot.forEach((doc) => {
  console.log(doc.id, doc.data())
})

// UPDATE
await updateDoc(doc(db, 'companies', 'acme-corp'), {
  industry: 'FinTech'
})

// DELETE
await deleteDoc(doc(db, 'companies', 'acme-corp'))
```

### Realtime Listeners

```typescript
import { onSnapshot } from 'firebase/firestore'

// Listen to document changes
const unsubscribe = onSnapshot(
  doc(db, 'companies', 'acme-corp'),
  (doc) => {
    console.log('Current data:', doc.data())
  }
)

// Listen to collection changes
const unsubscribe = onSnapshot(
  query(collection(db, 'companies'), where('industry', '==', 'Technology')),
  (snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added') {
        console.log('New:', change.doc.data())
      }
      if (change.type === 'modified') {
        console.log('Modified:', change.doc.data())
      }
      if (change.type === 'removed') {
        console.log('Removed:', change.doc.data())
      }
    })
  }
)

// Stop listening
unsubscribe()
```

### Batch Operations

```typescript
import { writeBatch } from 'firebase/firestore'

const batch = writeBatch(db)

batch.set(doc(db, 'companies', 'company1'), { name: 'Company 1' })
batch.update(doc(db, 'companies', 'company2'), { industry: 'Tech' })
batch.delete(doc(db, 'companies', 'company3'))

await batch.commit()
```

**Full API Reference**: https://firebase.google.com/docs/reference/js/firestore_

---

