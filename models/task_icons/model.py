import os
import cv2
import torch
import pandas as pd
import torch.optim as optim

from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.transforms import functional

NET_FILENAME = "task_icons_net.pth"


class TaskIconTypes:
    EVOLUTION = 0
    HATCH_ANTS = 1
    GET_EXOTIC_PEA_REWARD = 2
    LADYBUG = 3
    FIND_EXOTIC_PEA = 4
    LACK_OF_FUNGUS = 5
    CAVE_CHALLENGE = 6
    MINE_CAVE = 7
    DUEL_OF_QUEENS = 8
    HATCH_INSECTS = 9
    HATCH_INSECT_FODDER = 10
    SOLDIERS_REFORM = 11
    PATH_TO_BUILDINGS = 12
    WARZONE_CUSTOMIZATION = 13


class TaskIconsNet(nn.Module):
    """Neural network, based on LeNet5"""
    def __init__(self, num_classes):
        super().__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(6),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(400, 120)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(120, 84)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(84, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc1(out)
        out = self.relu1(out)
        out = self.fc2(out)
        return out


class TaskIconsDataset(Dataset):
    def __init__(self, root_dir="", csv_file=None, transform=None):
        """
        :param root_dir (string): Directory with all the images
        :param csv_file (string): Path to the csv file with annotations
        :param transform (callable): Optional transform to be applied on a sample
        """
        self.root_dir = root_dir
        self.transform = transform
        self.icons_data = pd.read_csv(os.path.join(self.root_dir, csv_file))

    def __len__(self):
        return len(self.icons_data)

    def __getitem__(self, idx):
        image_name = os.path.join(self.root_dir, self.icons_data.iloc[idx, 0])
        image = cv2.imread(image_name)

        if self.transform:
            image = self.transform(image)

        icon_class = self.icons_data.iloc[idx]["class_id"]
        icon_sample = {"filename": image_name, "image": image, "class": icon_class}
        return icon_sample


class TaskIconsModel:
    def __init__(self, root_dir="", batch_size=4):
        self.net = TaskIconsNet(num_classes=14)
        self.is_net_loaded = False
        self.root_dir = root_dir

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)

        self.train_transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.Grayscale(),
            transforms.ToTensor(),
            transforms.Normalize(mean=0.5, std=0.5),
        ])
        self.train_dataset = TaskIconsDataset(
            root_dir=root_dir,
            csv_file="train.csv",
            transform=self.train_transform
        )
        self.train_dataloader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

        self.test_transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.Grayscale(),
            transforms.ToTensor(),
            transforms.Normalize(mean=0.5, std=0.5),
        ])
        self.test_dataset = TaskIconsDataset(
            root_dir=root_dir,
            csv_file="test.csv",
            transform=self.test_transform
        )
        self.test_dataloader = DataLoader(self.test_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    def train(self, epochs_count):
        print("Train starts")

        for epoch in range(epochs_count):  # loop over the dataset multiple times
            running_loss = 0.0
            for i, data in enumerate(self.train_dataloader, 0):
                inputs, labels = data["image"], data["class"]

                # zero the parameter gradients
                self.optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.net(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 20 == 0:  # print every 20 mini-batches
                    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 20:.3f}')
                    running_loss = 0.0

        self.is_net_loaded = True

    def load_network(self):
        if not self.is_net_loaded:
            self.net.load_state_dict(torch.load(
                os.path.join(self.root_dir, NET_FILENAME)
            ))
            self.is_net_loaded = True

    def test(self):
        self.load_network()

        print("Test starts")
        test_errors = 0
        for i, data in enumerate(self.test_dataloader, 0):
            names, inputs, labels = data["filename"], data["image"], data["class"]

            outputs = self.net(inputs)
            _, predicted = torch.max(outputs, 1)
            for name, pred, label in zip(names, predicted, labels):
                print(f"{name}: actual {pred}, expected {label}")
                if pred != label:
                    test_errors += 1

        print(f"Errors: {test_errors}")

        return test_errors

    def save(self, filename="task_icons_net.pth"):
        print(f"Saving model to {filename}")

        torch.save(self.net.state_dict(), filename)

    def predict_single(self, image):
        self.load_network()

        image = functional.to_pil_image(image)
        image = self.test_transform(image)
        outputs = self.net(image.unsqueeze(0))
        _, predicted = torch.max(outputs, 1)
        return predicted[0]


if __name__ == "__main__":
    best_model = None
    best_errors = torch.inf
    best_epochs = 0
    epochs_grid = [2, 5, 10, 15, 20, 25, 30]

    for epochs in epochs_grid:
        model = TaskIconsModel(batch_size=4)
        model.train(epochs_count=epochs)
        errors = model.test()

        if errors < best_errors:
            best_model = model
            best_errors = errors
            best_epochs = epochs

    best_model.save(filename=NET_FILENAME)

    print(f"Best errors: {best_errors}, best epochs: {best_epochs}")
