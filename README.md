# HospitalManagementAWS

This project will re-create the project found in my HospitalManagement repository but in aws.<br>
See original project link <a href="https://github.com/justirack/HospitalManagement">here</a> <br>
The project will use APIGateway to create the endpoints where requests will be sent, and will be backed by lambda functions. Data will be stored in multiple dynamoDB tables, with one for each of patients, doctors and appointments respectively.

# Tentative Architecture
The following draw.io diagram contains the initial architecture diagram for patients. The diagram will be updated to include doctors and appointments once patients are complete.
Link to diagrams <a href="https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Hospital%20Manager%20AS.drawio.svg#R7Vtbb%2Bo4EP41PC6Knftj6eWsVrtSV3045zwhk7hgNcQoMbf99WsTGxIbShoISSWoVMVjZ%2BLM93mYGZuB%2FTjf%2FMjQYvYPjXEygFa8GdhPAwhDx%2BP%2FhWBbCFzXLgTTjMSFCBwEb%2BQ%2FLIWWlC5JjPPKQEZpwsiiKoxomuKIVWQoy%2Bi6OuydJtWnLtBUPtE6CN4ilGBj2E8Ss1khDdzS6D8xmc7Uk4Ele%2BZIDZaCfIZiui6J7OeB%2FZhRyoqr%2BeYRJ8J2yi7FfS8nevcTy3DK6tyA4V%2FJvxu6isc%2F0cfza5SBUfKHU2hZoWQpX1hOlm2VBTK6TGMslICBPVrPCMNvCxSJ3jWHnMtmbJ7IbnNScp4rnDG8KYnkJH9gOscs2%2FIhstcPhm5xj6QMUBZcHwAAnhwzKxnfU6RBEvTpXvnBLvxCmuYLZoLnzUSXLCEpftzz0OLmiFE%2B25lONIQJCGfW32iCk1eaE0ZoyvsmlDE6Lw14SMhUdDAqrItkK%2BImxVnV3JxTC%2FH8%2BWYqVt8QrXN7iBZkPEUMrxE34OidJMkjTWi2m6b9FD74jriV3xATrlL1pTTF1wEQQK%2BCn2eb%2BPmWCZ%2FfFnr2EfReFoiJ1%2BdXUYa5tQxA8w%2FMopnE7ii67%2FRgPm5a%2FvciZnXKtBoSI8sKnCcBIsvoB9YGt80cMXfpbQFUbfny4pEoXxQv%2Bk42Yh6jBSVCy%2FOKK8tP088Z4jTejW2HTMDtmEyuQSbJpPGORxyYMe8jMWIczv46iQTNJzEavy%2FTqHiCTs8XN3Btp1VHYSvHoLB1wnrYwpaw9c67ec7uBxFWCFsnKM9JVDX24dvS%2BsxIOV1mEf5kKtJnMZRNMTtPRxyrMOaEyUsmdY%2BYVMkynHAOr6rBzzE7yye87lb6HlHHqiK6R1ipKN5b3lUOVnRFblURDDRFhWEMRTvY96%2FdnAn%2B56v8vrTPLG0X6Es76HZpB9de2nhD2C%2FZI65%2FCzmPXIvW06Y07GlbarzijPBXEkgWspS%2F3q9yo6RJNA%2Bqdq1tuaUra%2B5v3Jr%2Bxu%2BXv4Gav9EzgNr%2Bxtf8jXdbfxMa9GRoIoj5sMNz53ryHvuceJuiOR3HE9PbwGffHgWtehsv1GjgHAkSocnC4BPCXeRtFA377G4OHuZ3xcHcxN34Nd1N2Gt3A0Knmbtxzylq2d0AtcROpMQZ10%2Fw6p4Uf4%2BkeB9KdZUUA7NApuJlSSWU3NPihmlxbXTbip2BWUDT0MV3TL%2BWD3WPaY3K%2FxcjFBVZgE4TmbBmZKFI3ZPQwghh3YaZjO9oiqzbZjLALJBeKfRV1xeHvt0SFNQt7akv1Z4w1NdqezCwh8APDx%2B3YSysMx94tyXs1au%2B1yLsBRyDdTkGesUxPS8yuFC7ngM6JpVZQK4kWMtFfN9z%2FC7plR3UDNZaS6%2FM6rUKwAsi3XOrhrlVbWhbi8PNym8V2juiX8usOkcUHqutXSWeaGuryQ9uHAHXzdH6Vf31tMzKbbq5red6zo03txUh%2B8fQCzgV1I14%2B0UqV8uqXAiHAShlVQ0ppnlF1wqHYflz2%2F0GeOwI3nWqTd1um4O6G1mKnz2hne1eyZc53hlFbTPrWB2zlGjFOMH3ROubJFp7Z9hVogVPn%2B68J1oXJVpO2PEBMGiW%2BRS0hY%2B4I%2Fq1RKt7RI%2FV2HoRxp46ZLPfeLhNcKIo%2F93yLHil2MTTDvXdPM%2Fq7aHTCzhV96CoIl9PSKXvMrlOw6Nbvl2NWRxbm0vbpDILhpeSqh%2BplIrkzzOrZ7950FPtpszSN78MRY2ZJU707X9nWgw%2F%2FFjXfv4f">here</a>


# Endpoint Request Specifications
## patient/add
The add patient endpoint expects the patients first name, last name and date of birth in <code>yyyy-mm-dd</code> format.<br>
See sample json below:
 
``` json
{
  "first_name":"Justin",
  "last_name":"Rackley",
  "date_of_birth":"2002-02-09"
}
```
