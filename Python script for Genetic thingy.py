import json

valid_pgx_results = ["PM", "IM", "NM", "RM", "URM"]
valid_slco181_pgx_results = ["PF", "DF", "NF"]
genes = ["CYP3A5", "CYP3A4", "CYP2D6", "CYP2C9", "CYP2C19"]

class Patient:
    def __init__(self, name):
        self.name = name
        self.results = {}

    def add_results(self, gene_results):
        for gene, result in gene_results.items():
            self.results[gene] = result

    def display_results(self):
        print(f"\n{self.name}'s Results:")
        for gene, result in self.results.items():
            print(f"{gene}: {result}")

def prints():
    print("=" * 80 + "\n")
    print("Select an option:\n")
    print("1: Add Patient")
    print("2: Check Patient Data")
    print("3: Assign Drug\n")
    print("=" * 80)

def check_result(result):
    if result in valid_pgx_results:
        return True
    return False

def get_result(gene):
    success = check_result(gene)
    return success

def main():
    patients = {}

    while True:
        prints()
        choice = input()

        match choice:
            case "1":
                patient_name = input("Please enter patient name: ")
                print("For each of the following please enter either:")

                for index, result in enumerate(valid_pgx_results, 1):
                    print(f'{index}: {result}')
                
                results = {}
                
                for gene in genes:
                    gene_result = input(f"Enter PGx results for {gene}: ")
                    success = get_result(gene_result)
                    while success == False:
                        print("Invalid result.")
                        gene_result = input(f"Enter PGx results for {gene}: ")
                        success = get_result(gene_result)

                    results[gene] = gene_result

                SLCO181_RESULTS = input("Enter PGx results for SLCO181: ")
                while not (SLCO181_RESULTS in valid_slco181_pgx_results):
                    print("Invalid result.")
                    SLCO181_RESULTS = input("Enter PGx results for SLCO181: ")
                
                results["SLCO181"] = SLCO181_RESULTS
                
                new_patient = Patient(patient_name)
                new_patient.add_results(results)
                
                patients[patient_name.lower()] = new_patient

                new_patient.display_results()

                input("Press any key to continue..")
                pass

            case "2":
                patient_name = input("Please enter patient name: ")

                patient_name_lower = patient_name.lower()
                if patient_name_lower in patients:
                    patients[patient_name_lower].display_results()
                else:
                    print("Patient not found.")
                
                input("Press any key to continue..")
                pass

            case "3":
                with open('drug_data.json', "r") as f:
                    drug_data = json.load(f)

                patient_name = input("Please enter patient name: ")
                patient_name_lower = patient_name.lower()

                if patient_name_lower not in patients:
                    print("Patient does not exist.")
                    break
                
                drug_name = input("Please enter drug name: ")
                if not (drug_name.lower() in drug_data.keys()):
                    print("Drug does not exist.")
                    break

                drug = drug_data[drug_name.lower()]
                patient_data = patients[patient_name_lower].results
                for gene, result in patient_data.items():
                    if not (drug.get(gene, {}).get(result, "N/A") == "N/A"):
                        print(f"Recommendation for {gene} ({result}): {drug[gene][result]}")

                input("Press any key to continue..")
                pass

            case _:
                print("Please select a valid option (1 or 2).")

main()
