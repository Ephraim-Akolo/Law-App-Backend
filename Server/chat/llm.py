import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# check if storage already exists
PERSIST_DIR = "./storage"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('.env', override=True)

# if not os.path.exists(PERSIST_DIR):
#     # load the documents and create the index
#     documents = SimpleDirectoryReader("./dataset/").load_data(show_progress=True)
#     index = VectorStoreIndex.from_documents(documents)
#     # store it for later
#     index.storage_context.persist(persist_dir=PERSIST_DIR)
# else:
#     # load the existing index
#     storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
#     index = load_index_from_storage(storage_context)

# load the existing index
storage_context1 = StorageContext.from_defaults(persist_dir=PERSIST_DIR+'1')
storage_context2 = StorageContext.from_defaults(persist_dir=PERSIST_DIR+'2')
index1= load_index_from_storage(storage_context1)
index2= load_index_from_storage(storage_context2)


def get_engine(model_number=1):
    # Either way we can now query the index
    if model_number == 1:
        return index1.as_query_engine()
    return index2.as_query_engine()


if __name__ == "__main__":
    response = get_engine(2).query("if someone strangles another person to death, what would you recommend for judgement?")
    print(response)